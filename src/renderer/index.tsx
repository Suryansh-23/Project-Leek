import { render } from 'react-dom';
import App from './App';

window.location.hash = '/';
render(<App />, document.getElementById('root'));
