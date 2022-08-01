import styles from "./Sentiment.module.css";

const  Sentiment = (props) => {
    console.log(props.newSentiment)
    return (
        <>
            {props.newSentiment.sentiment === null && <p className={`${styles.sentiment}`}>Loading</p>}
            {/* {props.newSentiment.sentiment === 'None' && <p>None</p>} */}
            {props.newSentiment.sentiment === 0 && <p className={`${styles.sentiment} ${styles.neutralSentiment}`}>Weekly Sentiment: Neutral</p>}
            {props.newSentiment.sentiment > 0 && <div className={`${styles.sentiment} ${styles.positiveSentiment}`}>Weekly Sentiment: Positive</div>}
            {props.newSentiment.sentiment < 0 && <div className={`${styles.sentiment} ${styles.negativeSentiment}`}>Weekly Sentiment: Negative</div>}
        </>
    )
};

export default Sentiment;