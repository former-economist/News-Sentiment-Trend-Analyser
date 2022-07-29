import styles from "./Sentiment.module.css";

const  Sentiment = (props) => {
    console.log(props.newSentiment)
    return (
        <>
            {props.newSentiment.sentiment === null && <p className={styles.sentiment}>Loading</p>}
            {props.newSentiment.sentiment > 0 && <div className={styles.positiveSentiment}></div>}
            {props.newSentiment.sentiment < 0 && <div className={styles.negativeSentiment}></div>}
        </>
    )
};

export default Sentiment;