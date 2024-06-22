import "./SearchResult.css";


export const SearchResult = (props) => {
    return (
      <div
        className="search-result"
        onClick={(e) => props.setDestination(props.result)}
      >
        {props.result}
      </div>
    );
  };