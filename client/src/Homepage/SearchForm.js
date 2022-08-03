import { useState } from "react";
import styles from "./SearchForm.module.css";


const SearchForm = (props) => {
  const [restrictedWord, setRestrictedWord] = useState([]);
  const [searchTerm, setSearchTerm] = useState();
  const [validSearchTerm, setValidSearchTerm] = useState(false);
  const [formTouched, setFormTouched] = useState(false)

  const searchTermHandler = (e) => {
    setSearchTerm(e.target.value);
  };

  const restrictedTermHandler = (e, index) => {
    const { name, value } = e.target;

    const list = [...restrictedWord];
    list[index][name] = value;

    setRestrictedWord(list);
  };

  const addRestrictedWordHandler = () => {
    setRestrictedWord([...restrictedWord, { blockedWord: "" }]);
  };

  const removeRestrictedWordHandler = (index) => {
    const list = [...restrictedWord];
    list.splice(index, 1);
    setRestrictedWord(list);
  };

  const createRestrictedTermList = () => {
    let restList = [...restrictedWord];
    let finalList = [];
    for (let i = 0; i < restList.length; i++) {
      finalList.push(restList[i].blockedWord);
    }
    return finalList;
  };

  const isSearchTermValid = !validSearchTerm && formTouched

  const submitHandler = (e) => {
    e.preventDefault();
    setFormTouched(true)
    const copy = searchTerm.slice()
    if ((copy.trim()).length > 1) {
      const queryData = {
        topic: searchTerm,
        "blocked-words": createRestrictedTermList(),
        token: "",
      };
      props.onSubmitQueryData(queryData);
      setSearchTerm("");
      setRestrictedWord([]);
      setFormTouched(false)
    }
    else{
      setValidSearchTerm(false)
      return;
    }
    

    // toResults('/result');
  };

  return (
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
              onChange={(e) => restrictedTermHandler(e, i)}
            ></input>
            <input
              className={`${styles.button}`}
              type="button"
              value="Remove"
              onClick={() => removeRestrictedWordHandler(i)}
              maxLength='20'
            />
          </div>
        );
      })}
      <div>
        <button className={`${styles.input} ${styles.button} ${styles.bigButton}`} type="button" value="Add" onClick={addRestrictedWordHandler}>
          Block Term
        </button>
      </div>
      <div>
        <button className={`${styles.input} ${styles.button} ${styles.bigButton} ${styles.submit}`} type="submit">Search</button>
      </div>
      {isSearchTermValid && (<p>Search term cannot contain only white spaces</p>)}
    </form>
  );
};

export default SearchForm;
