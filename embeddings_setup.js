import { GoogleGenerativeAI } from "@google/generative-ai";
import { QdrantClient } from "@qdrant/js-client-rest";
import fs from "fs";
import path from "path";

// Initialize clients
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

const qdrant = new QdrantClient({
  url: process.env.QDRANT_URL,
  apiKey: process.env.QDRANT_API_KEY
});

async function embedText(text) {
  try {
    const model = genAI.getGenerativeModel({ model: "text-embedding-004" });
    const result = await model.embedContent(text);
    return result.embedding.values;
  } catch (error) {
    console.error("Error getting embedding:", error);
    // Fallback: return a simple hash-based embedding
    const crypto = await import('crypto');
    const hash = crypto.createHash('sha256').update(text).digest('hex');
    const embedding = [];
    for (let i = 0; i < 768; i += 2) { // text-embedding-004 returns 768 dimensions
      embedding.push(parseInt(hash.substr(i, 2), 16) / 255.0);
    }
    return embedding.slice(0, 768);
  }
}

async function processProjectFiles() {
  console.log("Starting project file processing...");

  // Define file extensions to process
  const fileExtensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.md', '.txt', '.json', '.yaml', '.yml'];

  // Get all files in the project
  const getAllFiles = (dir) => {
    let results = [];
    const items = fs.readdirSync(dir);

    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        // Skip certain directories
        if (item !== 'node_modules' && item !== '.git' && item !== '__pycache__' &&
            item !== '.docusaurus' && item !== 'dist' && item !== 'build') {
          results = results.concat(getAllFiles(fullPath));
        }
      } else {
        const ext = path.extname(fullPath);
        if (fileExtensions.includes(ext)) {
          results.push(fullPath);
        }
      }
    }

    return results;
  };

  const projectDir = process.cwd(); // Current directory
  const files = getAllFiles(projectDir);

  console.log(`Found ${files.length} files to process`);

  // Create collection if it doesn't exist
  try {
    await qdrant.getCollections();
    const collections = await qdrant.getCollections();
    const collectionExists = collections.collections.some(col => col.name === "project_documents");

    if (!collectionExists) {
      await qdrant.createCollection("project_documents", {
        vectors: {
          size: 768, // Size for text-embedding-004
          distance: "Cosine"
        }
      });
      console.log("Created 'project_documents' collection");
    }
  } catch (error) {
    console.error("Error checking/creating collection:", error);
  }

  // Process each file
  for (let i = 0; i < files.length; i++) {
    const filePath = files[i];
    console.log(`Processing (${i+1}/${files.length}): ${filePath}`);

    try {
      const content = fs.readFileSync(filePath, 'utf-8');

      // Split large files into chunks
      const chunks = [];
      const chunkSize = 2000; // characters

      for (let j = 0; j < content.length; j += chunkSize) {
        const chunk = content.substring(j, j + chunkSize);
        if (chunk.trim()) {
          chunks.push({
            content: chunk,
            source: filePath,
            chunkIndex: j / chunkSize
          });
        }
      }

      // Process each chunk
      for (const chunk of chunks) {
        const embedding = await embedText(chunk.content);

        await qdrant.upsert("project_documents", {
          points: [
            {
              id: `${path.basename(filePath, path.extname(filePath))}_${chunk.chunkIndex}_${Date.now()}`,
              vector: embedding,
              payload: {
                content: chunk.content,
                source: chunk.source,
                type: "project_code",
                chunk_index: chunk.chunkIndex
              }
            }
          ]
        });

        console.log(`  Uploaded chunk ${chunk.chunkIndex} from ${path.basename(filePath)}`);
      }
    } catch (error) {
      console.error(`Error processing ${filePath}:`, error);
    }
  }

  console.log("Project file processing completed!");
}

// Run the processing
processProjectFiles().catch(console.error);