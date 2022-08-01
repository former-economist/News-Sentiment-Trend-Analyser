import styles from "./SearchResult.module.css";

const SearchResult = (props) => {
  const { headline, publisher, date, url, sentiment } = props;
  return (
    <>
      {sentiment === 0 && (
        <li className={`${styles.article} ${styles.neutral}`}>
          
            <h2><a
            href={url}
            className={styles.Neutral}
            target="_blank"
            rel="noopener noreferrer"
          >{headline}</a></h2>
          
          <p className={`${styles.neutralP}`}>{publisher}</p>
          <p className={`${styles.neutralP}`}>{date}</p>
        </li>
      )}
      {sentiment > 0 && (
        <li className={`${styles.article} ${styles.positive}`}>
          
            <h2><a
            href={url}
            className={styles.Positive}
            target="_blank"
            rel="noopener noreferrer"
          >{headline}</a></h2>
          
          <p className={`${styles.positiveP}`}>{publisher}</p>
          <p className={`${styles.positiveP}`}>{date}</p>
        </li>
      )}
      {sentiment < 0 && (
        <li className={`${styles.article} ${styles.negative}`}>
          
            <h2><a
            href={url}
            className={styles.Negative}
            target="_blank"
            rel="noopener noreferrer"
          >{headline}</a></h2>
          
          <p className={`${styles.negativeP}`}>{publisher}</p>
          <p className={`${styles.negativeP}`}>{date}</p>
        </li>
      )}
    </>
  );
};

export default SearchResult;
