import styles from "./SearchResult.module.css";

const SearchResult = (props) => {
  const { headline, publisher, date, url, sentiment } = props;

  function checkURLIsValid(inputURL){
    let checked = new URL(inputURL)
    if(['http:', 'https:'].includes(checked.protocol)){
      return true
    };
    return false
  };

  const isSafe = checkURLIsValid(url)
  
  return (
    <>
      {isSafe === true && sentiment === 0 && (
        <li className={`${styles.article} ${styles.neutral}`} title="Neutral">
          
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
      {isSafe && sentiment > 0 && (
        <li className={`${styles.article} ${styles.positive}`} title="Positive">
          
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
      {isSafe && sentiment < 0 && (
        <li className={`${styles.article} ${styles.negative}`} title="Negative">
          
            <h2><a
            href={checkURLIsValid(url) ? url : ""}
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
