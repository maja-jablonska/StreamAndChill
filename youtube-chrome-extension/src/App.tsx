import "./App.css";

import { Overlay } from "./Overlay/Overlay";

export const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <iframe
          title="youtube-vid"
          width="1000"
          height="600"
          src="https://www.youtube.com/embed/tgbNymZ7vqY"
        ></iframe>
        <Overlay />
      </header>
    </div>
  );
};

export default App;
