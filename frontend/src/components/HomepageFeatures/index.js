import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Advanced Physical AI Concepts',
    Svg: require('@site/static/img/undraw_robotics.svg').default,
    description: (
      <>
        Explore cutting-edge concepts in Physical AI that combine robotics, artificial intelligence,
        and real-world interaction for next-generation autonomous systems.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics',
    Svg: require('@site/static/img/undraw_ai_robot.svg').default,
    description: (
      <>
        Learn about humanoid robots that mimic human movement, behavior, and cognitive processes
        with sophisticated control systems and AI integration.
      </>
    ),
  },
  {
    title: 'Interactive Learning',
    Svg: require('@site/static/img/undraw_learning.svg').default,
    description: (
      <>
        Engage with AI-powered learning tools, real-time translation, and personalized content
        that adapts to your learning style and experience level.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
