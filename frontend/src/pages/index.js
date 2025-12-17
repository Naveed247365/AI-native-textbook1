import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.animatedBackground}>
          <div className={styles.animatedCircle}></div>
          <div className={styles.animatedCircle}></div>
          <div className={styles.animatedCircle}></div>
        </div>
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <div className={styles.badge}>🤖 AI-POWERED LEARNING</div>
            <Heading as="h1" className="hero__title">
              {siteConfig.title}
            </Heading>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
            <div className={styles.buttons}>
              <Link
                className="button button--secondary button--lg"
                to="/docs/intro">
                Explore Concepts
              </Link>
              <Link
                className="button button--primary button--lg"
                to="/docs/intro">
                Start Learning
              </Link>
            </div>
          </div>
          <div className={styles.heroVisual}>
            <div className={styles.robotIcon}>🤖</div>
          </div>
        </div>
      </div>
    </header>
  );
}

function HomepageHighlights() {
  return (
    <section className={styles.highlights}>
      <div className="container">
        <div className="row">
          <div className="col col--4">
            <div className={clsx(styles.highlightCard, styles.card1)}>
              <div className={styles.highlightIcon}>🧠</div>
              <h3>AI-Powered Learning</h3>
              <p>Interactive AI assistant that helps you understand complex robotics concepts through contextual explanations and real-time Q&A.</p>
            </div>
          </div>
          <div className="col col--4">
            <div className={clsx(styles.highlightCard, styles.card2)}>
              <div className={styles.highlightIcon}>🌐</div>
              <h3>Global Accessibility</h3>
              <p>Real-time translation support in multiple languages including Urdu, making advanced robotics education accessible worldwide.</p>
            </div>
          </div>
          <div className="col col--4">
            <div className={clsx(styles.highlightCard, styles.card3)}>
              <div className={styles.highlightIcon}>🎯</div>
              <h3>Personalized Content</h3>
              <p>Content adapts to your background and experience level, providing tailored learning paths for both beginners and advanced learners.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function CTASection() {
  return (
    <section className={styles.ctaSection}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <div className={styles.ctaContent}>
              <h2>Ready to Dive into Physical AI & Humanoid Robotics?</h2>
              <p>Join thousands of learners exploring the future of robotics with our AI-powered interactive textbook.</p>
              <div className={styles.ctaButtons}>
                <Link
                  className="button button--primary button--lg"
                  to="/docs/category/getting-started">
                  Begin Your Journey
                </Link>
                <Link
                  className="button button--secondary button--lg"
                  to="/docs/intro">
                  View Curriculum
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Physical AI & Humanoid Robotics`}
      description="Interactive learning platform for Physical AI and Humanoid Robotics with AI-powered assistance">
      <HomepageHeader />
      <HomepageHighlights />
      <CTASection />
      <main className={styles.mainContent}>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
