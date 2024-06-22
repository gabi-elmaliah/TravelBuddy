import "./SearchResultsList.css";
import { SearchResult } from "./SearchResult";


const SearchResultsList=(props)=>
    {

        return (
            <div className="results-list">
              {props.results.map((result, id) => {
                return <SearchResult result={result.name} key={id} setDestination={props.setDestination}/>;
              })}
            </div>
          );
    

    };

    export default SearchResultsList;
