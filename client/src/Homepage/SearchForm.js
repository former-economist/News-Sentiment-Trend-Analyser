import { useState } from "react";
import styles from "./SearchForm.module.css";


const SearchForm = (props) => {
  const [restrictedWord, setRestrictedWord] = useState([]);
  const [searchTerm, setSearchTerm] = useState();

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

  const submitHandler = (e) => {
    e.preventDefault();
    const queryData = {
      topic: searchTerm,
      "blocked-words": createRestrictedTermList(),
      token: "",
    };
    props.onSubmitQueryData(queryData);
    setSearchTerm("");
    setRestrictedWord([]);

    // toResults('/result');
  };

  return (
    <form className={styles.form} onSubmit={submitHandler}>
      <div>
        <label>
          <input
            className={styles.input}
            type="text"
            value={searchTerm}
            placeholder="Search"
            onChange={searchTermHandler}
          />
        </label>
      </div>
      {restrictedWord.map((data, i) => {
        return (
          <div key={i}>
            <input
              className={styles.input}
              type="text"
              name="blockedWord"
              value={data.blockedWord}
              placeholder="Restricted term"
              onChange={(e) => restrictedTermHandler(e, i)}
            ></input>
            <input
              className={styles.button}
              type="button"
              value="Remove"
              onClick={() => removeRestrictedWordHandler(i)}
            />
          </div>
        );
      })}
      <div>
        <button className={styles.button} type="button" value="Add" onClick={addRestrictedWordHandler}>
          Add restricted Term
        </button>
      </div>
      <div>
        <button className={styles.button} type="submit">Submit</button>
      </div>
    </form>
  );
};

export default SearchForm;
