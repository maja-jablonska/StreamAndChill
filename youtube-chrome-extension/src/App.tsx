import "./App.css";

import { Overlay } from "./Overlay/Overlay";

export const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <iframe
          title="youtube-vid"
          width="1440"
          height="850"
          src="https://www.youtube.com/embed/W86cTIoMv2U"
        ></iframe>
        <Overlay />
      </header>
    </div>
  );
};

export default App;
