

import { Redirect, Route, Switch } from 'react-router-dom';
import Homepage from './Homepage/Homepage';
import Results from './ResultPage/Results';
import styles from './App.module.css'

function App() {
  return (
    <div className={styles.div}>
      <Switch>
        <Route path="/" exact>
          <Redirect to="/homepage" />
        </Route>
        <Route path="/homepage">
          <Homepage />
        </Route>
        <Route path="/result">
          <Results />
        </Route>
      </Switch>
      
    </div>
  );
}

export default App;
