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
        {/* Animated background elements */}
        <div className={styles.animatedBackground}>
          <div className={clsx(styles.animatedCircle, styles.circle1)}></div>
          <div className={clsx(styles.animatedCircle, styles.circle2)}></div>
          <div className={clsx(styles.animatedCircle, styles.circle3)}></div>
          <div className={clsx(styles.animatedParticle, styles.particle1)}></div>
          <div className={clsx(styles.animatedParticle, styles.particle2)}></div>
          <div className={clsx(styles.animatedParticle, styles.particle3)}></div>
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
                Start Learning Physical AI
              </Link>
              <Link
                className="button button--primary button--lg"
                to="/docs/humanoid-robotics/intro">
                Explore Humanoid Robotics
              </Link>
            </div>
          </div>
          <div className={styles.heroVisual}>
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
              </div>
              <div className={styles.humanoidArms}>
                <div className={clsx(styles.humanoidArm, styles.humanoidLeftArm)}></div>
                <div className={clsx(styles.humanoidArm, styles.humanoidRightArm)}></div>
              </div>
              <div className={styles.humanoidLegs}>
                <div className={clsx(styles.humanoidLeg, styles.humanoidLeftLeg)}></div>
                <div className={clsx(styles.humanoidLeg, styles.humanoidRightLeg)}></div>
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
              <p>Master the principles of embodied intelligence where AI meets physical systems, enabling robots to interact with the real world.</p>
            </div>
          </div>
          <div className="col col--4">
            <div className={clsx(styles.highlightCard, styles.card2)}>
              <div className={styles.highlightIcon}>🦾</div>
              <h3>Humanoid Robotics</h3>
              <p>Learn how to design, control, and program humanoid robots that can walk, balance, and interact with human environments.</p>
            </div>
          </div>
          <div className="col col--4">
            <div className={clsx(styles.highlightCard, styles.card3)}>
              <div className={styles.highlightIcon}>🧠</div>
              <h3>Embodied Intelligence</h3>
              <p>Understand how intelligence emerges through the interaction between AI systems and their physical environment for superior robotic capabilities.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function FeaturesSection() {
  return (
    <section className={styles.featuresSection}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h2>Physical AI & Robotics Learning Features</h2>
          </div>
        </div>
        <div className="row">
          <div className="col col--4">
            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>🔬</div>
              <h3>Embodied Intelligence</h3>
              <p>Learn how AI systems gain intelligence through physical interaction with the environment, enabling superior robotic capabilities.</p>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>🦾</div>
              <h3>Humanoid Control Systems</h3>
              <p>Master advanced control algorithms for bipedal locomotion, balance, and human-like movement patterns.</p>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>🌐</div>
              <h3>Real-world Applications</h3>
              <p>Explore practical implementations of humanoid robots in manufacturing, healthcare, and service industries.</p>
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
              <h2>Begin Your Journey in Physical AI & Humanoid Robotics</h2>
              <p>Master the cutting-edge intersection of artificial intelligence and physical systems with our AI-powered interactive textbook.</p>
              <div className={styles.ctaButtons}>
                <Link
                  className="button button--primary button--lg"
                  to="/docs/intro">
                  Start Learning Now
                </Link>
                <Link
                  className="button button--secondary button--lg"
                  to="/docs/humanoid-robotics/intro">
                  Explore Robotics
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
      <main>
        <HomepageHighlights />
        <FeaturesSection />
        <CTASection />
      </main>
    </Layout>
  );
}