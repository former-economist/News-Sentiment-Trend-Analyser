import SearchResult from "./SearchResult";
import styles from "./SearchResultList.module.css";

const SearchResultList = (props) => {
  return (
    <ul className={styles.searchlist}>
      {props.SearchResult.result.map((finding) => (
        <SearchResult
          key={finding.id}
          headline={finding.headline}
          publisher={finding.publisher}
          date={finding.publish_date}
          url={finding.url}
          sentiment={finding.sentiment}
        />
      ))}
    </ul>
  );
};

export default SearchResultList;
