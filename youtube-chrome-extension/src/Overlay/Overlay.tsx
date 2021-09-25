import { useEffect, useState } from "react";
import { CountdownOverlay } from "../CountdownOverlayCSS/CountdownOverlay";
import { GetReadyOverlay } from "../GetReadyOverlay/GetReadyOverlay";

import "./Overlay.css";
const DURATION_STEP_ONE = 6500;
const DURATION_STEP_TWO = 7000;
const DURATION_STEP_THREE = 3500;

export const Overlay = () => {
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
    <div className="overlayContainer">
      {step === 1 && <GetReadyOverlay text={textStepOne} />}
      {step === 2 && <GetReadyOverlay text={textStepTwo} />}
      {step === 3 && <CountdownOverlay />}
    </div>
  );
};
