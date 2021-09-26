import "./App.css";

import { Overlay } from "./Overlay/Overlay";

export const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <img src="https://natureconservancy-h.assetsadobe.com/is/image/content/dam/tnc/nature/en/photos/Zugpsitze_mountain.jpg?crop=0,176,3008,1654&wid=4000&hei=2200&scl=0.752" alt=""/>
        <Overlay />
      </header>
    </div>
  );
};

export default App;
