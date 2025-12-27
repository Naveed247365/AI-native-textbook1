import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <div className={styles.badge}>
              <span>Physical AI Textbook</span>
            </div>
            <h1 className={styles.heroTitle}>
              Introduction to{' '}
              <span className={styles.heroTitleAccent}>Physical AI</span>
              {' & '}
              <span className={styles.heroTitleAccent}>Humanoid Robotics</span>
            </h1>
            <p className={styles.heroSubtitle}>
              Master the intersection of artificial intelligence and physical systems.
              Learn to build, program, and deploy humanoid robots with cutting-edge AI techniques.
            </p>
            <div className={styles.buttons}>
              <Link
                className="button button--primary button--lg"
                to="/docs/intro">
                Start Reading
              </Link>
              <Link
                className="button button--secondary button--lg"
                to="/docs/weekly-plan">
                View Curriculum
              </Link>
            </div>
          </div>
          <div className={styles.heroVisual}>
            <div className={styles.robotContainer}>
              <div className={styles.robotGlow}></div>
              <div className={styles.humanoidRobot}>
                <div className={styles.humanoidHead}>
                  <div className={clsx(styles.humanoidEye, styles.humanoidLeftEye)}></div>
                  <div className={clsx(styles.humanoidEye, styles.humanoidRightEye)}></div>
                  <div className={styles.humanoidMouth}></div>
                </div>
                <div className={styles.humanoidNeck}></div>
                <div className={styles.humanoidBody}>
                  <div className={styles.humanoidChestPanel}>
                    <div className={styles.humanoidChestLight}></div>
                  </div>
                  <div className={styles.humanoidArms}>
                    <div className={clsx(styles.humanoidArm, styles.humanoidLeftArm)}></div>
                    <div className={clsx(styles.humanoidArm, styles.humanoidRightArm)}></div>
                  </div>
                </div>
                <div className={styles.humanoidLegs}>
                  <div className={clsx(styles.humanoidLeg, styles.humanoidLeftLeg)}></div>
                  <div className={clsx(styles.humanoidLeg, styles.humanoidRightLeg)}></div>
                </div>
              </div>
            </div>
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
              <div className={styles.highlightIcon}>🤖</div>
              <h3>Physical AI Fundamentals</h3>
              <p>
                Understand how AI systems gain intelligence through physical interaction
                with the environment, enabling superior robotic capabilities.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className={clsx(styles.highlightCard, styles.card2)}>
              <div className={styles.highlightIcon}>🦾</div>
              <h3>Humanoid Robotics</h3>
              <p>
                Learn to design, control, and program humanoid robots that can walk,
                balance, and interact naturally with human environments.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className={clsx(styles.highlightCard, styles.card3)}>
              <div className={styles.highlightIcon}>🧠</div>
              <h3>Embodied Intelligence</h3>
              <p>
                Explore how intelligence emerges through the interaction between
                AI systems and their physical environment.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function FeaturesSection() {
  const features = [
    {
      icon: '🔬',
      title: 'ROS2 & Simulation',
      description: 'Master Robot Operating System 2 and simulation environments for development.',
    },
    {
      icon: '🎮',
      title: 'NVIDIA Isaac',
      description: 'Learn NVIDIA Isaac Sim and Isaac Lab for advanced robotics simulation.',
    },
    {
      icon: '👁️',
      title: 'Computer Vision',
      description: 'Implement vision systems for robot perception and navigation.',
    },
    {
      icon: '🎯',
      title: 'Motion Planning',
      description: 'Design motion planning algorithms for humanoid locomotion.',
    },
    {
      icon: '🔄',
      title: 'Reinforcement Learning',
      description: 'Apply RL techniques for robot skill acquisition and adaptation.',
    },
    {
      icon: '🛠️',
      title: 'Hands-on Projects',
      description: 'Build real-world applications with capstone projects.',
    },
  ];

  return (
    <section className={styles.featuresSection}>
      <div className="container">
        <h2 className={styles.sectionTitle}>What You'll Learn</h2>
        <p className={styles.sectionSubtitle}>
          A comprehensive curriculum covering all aspects of physical AI and humanoid robotics
        </p>
        <div className="row">
          {features.map((feature, idx) => (
            <div className="col col--4" key={idx}>
              <div className={styles.featureCard}>
                <div className={styles.featureIcon}>{feature.icon}</div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function StatsSection() {
  return (
    <section className={styles.statsSection}>
      <div className="container">
        <div className={styles.statsGrid}>
          <div className={styles.statItem}>
            <div className={styles.statNumber}>8</div>
            <div className={styles.statLabel}>Chapters</div>
          </div>
          <div className={styles.statItem}>
            <div className={styles.statNumber}>16</div>
            <div className={styles.statLabel}>Weeks</div>
          </div>
          <div className={styles.statItem}>
            <div className={styles.statNumber}>1</div>
            <div className={styles.statLabel}>Capstone</div>
          </div>
          <div className={styles.statItem}>
            <div className={styles.statNumber}>AI</div>
            <div className={styles.statLabel}>Powered</div>
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
        <div className={styles.ctaContent}>
          <h2>Ready to Build the Future?</h2>
          <p>
            Start your journey into Physical AI and Humanoid Robotics today.
            Our AI-powered learning platform adapts to your pace and style.
          </p>
          <div className={styles.ctaButtons}>
            <Link
              className="button button--primary button--lg"
              to="/docs/intro">
              Begin Learning
            </Link>
            <Link
              className="button button--secondary button--lg"
              to="/docs/capstone-project">
              View Capstone
            </Link>
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
      title="Physical AI & Humanoid Robotics"
      description="Interactive textbook for learning Physical AI and Humanoid Robotics with AI-powered assistance">
      <HomepageHeader />
      <main>
        <HomepageHighlights />
        <StatsSection />
        <FeaturesSection />
        <CTASection />
      </main>
    </Layout>
  );
}
