const SearchItem = (props) => {
    console.log(props.topic)
    console.log(props.sentiment)
    
    

    return(
    <li>
        <p>{props.topic}</p>
    </li>
    )
};

export default SearchItem;