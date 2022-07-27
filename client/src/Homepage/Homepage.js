// import { useHistory } from "react-router-dom";
import { useState } from "react";
import SearchForm from "./SearchForm";
import SearchList from "./SearchList";
import SearchResultList from "./SearchResultList";

import Sentiment from "./Sentiment";

import styles from "./Homepage.module.css"

const Homepage = (props) => {
    const [queries, setQueries] = useState([])
    const [newResult, setNewResult] = useState({result : 1, sentiment : null, topic : null})
    const [isLoading, setIsLoading] = useState(false)

    const addQuery = (newData) => {
        setQueries((prevQueries)=>{
            return[...newData, ...prevQueries]
        })
    }

    async function fetchPostQueryHandler(enteredQueryData) {
        const queryData = {
            ...enteredQueryData
        };
        const response = await fetch('/search/', {
            method: 'POST',
            body: JSON.stringify(queryData),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        console.log(data)
        addQuery(data)
        setNewResult({result : 0})
        console.log(data)
    }; 

    console.log(newResult)

    return (
         <div className={styles.container}>
            <section>
                <SearchForm onSubmitQueryData={fetchPostQueryHandler}/>
            </section>
            <section>
                <SearchList queries={queries} newResult={newResult} setNewResult={setNewResult}/>
                
            </section>
            <section>
                {newResult.result === 0 && <p>Loading</p>}
                {(newResult.result).length > 1 && <Sentiment newSentiment={newResult}/>}
            </section>
            <section>
                {(newResult.result).length > 1 && <SearchResultList SearchResult={newResult}/>}
                
            </section>
        </div>
        
    );
};

export default Homepage;