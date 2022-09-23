import { useState } from "react";
import styles from "./SearchForm.module.css";

const SearchForm = (props) => {
  const [restrictedWord, setRestrictedWord] = useState([]);
  const [searchTerm, setSearchTerm] = useState();
  const [invalidSearchTerm, setInvalidSearchTerm] = useState(false);
  const [blockedSameSearch, setBlockedSameSearch] = useState(false);
  const [formTouched, setFormTouched] = useState(false);

  /**
   * Set state for search term.
   * @param {event} e 
   */
  const searchTermHandler = (e) => {
    setSearchTerm(e.target.value);
  };

  /**
   * Set restricted terms.
   * @param {event} e
   * @param {int} index - Index to be added
   */
  const restrictedTermHandler = (e, index) => {
    const { name, value } = e.target;

    const list = [...restrictedWord];
    list[index][name] = value;

    setRestrictedWord(list);
  };

  const addRestrictedWordHandler = () => {
    setRestrictedWord([...restrictedWord, { blockedWord: "" }]);
  };

  /**
   * Removes restricted term input field.
   * @param {int} index - Chosen input index to be changed.
   */
  const removeRestrictedWordHandler = (index) => {
    const list = [...restrictedWord];
    list.splice(index, 1);
    setRestrictedWord(list);
  };

  /**
   * Creates a list of restricted words.
   * @returns A list of restricted word from input.
   */
  const createRestrictedTermList = () => {
    let restList = [...restrictedWord];
    let finalList = [];
    for (let i = 0; i < restList.length; i++) {
      let blocked = restList[i].blockedWord.trim();
      if (blocked.length > 0) {
        finalList.push(blocked);
      }
    }
    return finalList;
  };

  const isSearchTermValid = invalidSearchTerm && formTouched;
  const isBlockedSameSearch = blockedSameSearch && formTouched;

  /**
   * Checks if restricted term is the same as search term.
   * @param {event} e - Submission event
   * @returns Boolean
   */

  function isRestrictedSameSearch(arr) {
    const copy = arr.slice();
    for (let i = 0; i < copy.length; i++) {
      copy[i].replace(/-/g, "");
      if (searchTerm.includes(copy[i]) || searchTerm.includes(copy[i] + "s")) {
        return false;
      }
    }
    return true;
  }

  const submitHandler = (e) => {
    e.preventDefault();
    props.setNewIntro(false); 
    props.setServer(true);
    setFormTouched(true);
    setInvalidSearchTerm(false);
    setBlockedSameSearch(false);
    const copy = searchTerm.slice();
    const restWords = createRestrictedTermList();
    if (isRestrictedSameSearch(restWords) === false) {
      setBlockedSameSearch(true);
      return;
    } else if (copy.trim().length > 1) {
      const queryData = {
        topic: searchTerm,
        "blocked-words": restWords,
        token: "",
      };
      props.onSubmitQueryData(queryData);
      setSearchTerm("");
      setRestrictedWord([]);
      setFormTouched(false);
    } else {
      setInvalidSearchTerm(true);
      return;
    }
  };

  return (
    <div>
      <form className={styles.form} onSubmit={submitHandler}>
        <div>
          <label>
            <input
              className={`${styles.input} ${styles.greyback}`}
              type="text"
              value={searchTerm}
              placeholder="Search"
              onChange={searchTermHandler}
              maxLength="50"
              required
              title="Insert a topic you would like to read news about."
            />
          </label>
        </div>
        {restrictedWord.map((data, i) => {
          return (
            <div key={i}>
              <input
                className={`${styles.input} ${styles.greyback}`}
                type="text"
                name="blockedWord"
                value={data.blockedWord}
                placeholder="Restricted term"
                required
                autoComplete="off"
                title="Enter restriced term that should not occur in article headlines."
                onChange={(e) => restrictedTermHandler(e, i)}
              ></input>
              <input
                className={`${styles.button} ${styles.removeButton}`}
                type="button"
                value="Remove"
                onClick={() => removeRestrictedWordHandler(i)}
                maxLength="20"
                title="Hit Remove to remove a blocked word from search."
              />
            </div>
          );
        })}
        <div>
          <button
            className={`${styles.input} ${styles.button} ${styles.bigButton} ${styles.blockButton}`}
            type="button"
            value="Add"
            onClick={addRestrictedWordHandler}
            title="Hit Add Blocked Word to exclude a term from occuring in result headlines."
          >
            Add Blocked Term
          </button>
        </div>
        <div>
          <button
            className={`${styles.input} ${styles.button} ${styles.bigButton} ${styles.submit}`}
            type="submit"
            title="Hit Submit to find result on input search term."
          >
            Search
          </button>
        </div>
        {isSearchTermValid && (
          <p>Search term cannot contain only white spaces</p>
        )}
        {isBlockedSameSearch && (
          <p>Search term and block term cannot be the same</p>
        )}
      </form>
    </div>
  );
};

export default SearchForm;
