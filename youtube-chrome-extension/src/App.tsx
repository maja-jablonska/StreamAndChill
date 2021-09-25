import { useEffect, useState } from "react";
import "./App.css";
import { CountdownOverlay } from "./CountdownOverlayCSS/CountdownOverlay";

import { GetReadyOverlay } from "./GetReadyOverlay/GetReadyOverlay";
const DURATION_STEP_ONE = 7000;
const DURATION_STEP_TWO = 7000;
const DURATION_STEP_THREE = 4000;

export const App = () => {
  const textStepOne = "It's time to focus on your health";
  const textStepTwo = "Ready to collect some oranges?";
  const [step, setStep] = useState(1);

  useEffect(() => {
    setTimeout(() => setStep(2), DURATION_STEP_ONE);
    setTimeout(() => setStep(3), DURATION_STEP_ONE + DURATION_STEP_TWO);
    setTimeout(
      () => setStep(4),
      DURATION_STEP_ONE + DURATION_STEP_TWO + DURATION_STEP_THREE
    );
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <iframe
          title="youtube-vid"
          width="1000"
          height="600"
          src="https://www.youtube.com/embed/tgbNymZ7vqY"
        ></iframe>
        {step === 1 && <GetReadyOverlay text={textStepOne} />}
        {step === 2 && <GetReadyOverlay text={textStepTwo} />}
        {step === 3 && <CountdownOverlay />}
      </header>
    </div>
  );
};

export default App;
