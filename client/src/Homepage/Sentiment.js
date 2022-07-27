

const  Sentiment = (props) => {
    console.log(props.newSentiment)
    return (
        <div>
            {props.newSentiment.sentiment === null && <p>Loading</p>}
            <p>Sentiment: {props.newSentiment.sentiment}</p>
        </div>
    )
};

export default Sentiment;