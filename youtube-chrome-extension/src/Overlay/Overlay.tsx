import { useEffect, useState } from "react";
import { BreathingAnimation } from "../BreathingAnimation/BreathingAnimation";
import { CountdownOverlay } from "../CountdownOverlayCSS/CountdownOverlay";
import { GetReadyOverlay } from "../GetReadyOverlay/GetReadyOverlay";

import "./Overlay.css";
const DURATION_STEP_ONE = 6500;
const DURATION_STEP_TWO = 7000 + DURATION_STEP_ONE;
const DURATION_STEP_THREE = DURATION_STEP_TWO + 3500;
const DURATION_STEP_FOUR = DURATION_STEP_THREE + 10000;

export const Overlay = () => {
  const textStepOne = "It's time to focus on your health";
  const textStepTwo = "Ready to collect some oranges?";
  const [step, setStep] = useState(1);

  useEffect(() => {
    setTimeout(() => setStep(2), DURATION_STEP_ONE);
    setTimeout(() => setStep(3), DURATION_STEP_TWO);
    setTimeout(() => setStep(4), DURATION_STEP_THREE);
    setTimeout(() => setStep(4), DURATION_STEP_FOUR);
  }, []);

  return (
    <div className="overlayContainer">
      {step === 1 && <GetReadyOverlay text={textStepOne} />}
      {step === 2 && <GetReadyOverlay text={textStepTwo} />}
      {step === 3 && <CountdownOverlay />}
      {step === 4 && <BreathingAnimation />}
    </div>
  );
};
