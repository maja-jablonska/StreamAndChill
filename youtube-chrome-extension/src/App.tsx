import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";

import { GetReadyOverlay } from "./GetReadyOverlay/GetReadyOverlay";

export const App = () => {
  const [showGetReadyOverlay, setShowGetReadyOverlay] = useState(true);
  setTimeout(() => setShowGetReadyOverlay(false), 6000);

  return (
    <div className="App">
      <header className="App-header">
        <iframe
          title="youtube-vid"
          width="1000"
          height="600"
          src="https://www.youtube.com/embed/tgbNymZ7vqY"
        ></iframe>
        {/* {showGetReadyOverlay && ( */}
        <GetReadyOverlay isShown={showGetReadyOverlay} />
        {/* )} */}
      </header>
    </div>
  );
};

export default App;
