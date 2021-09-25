import { useState } from "react";
import { Overlay } from "../Overlay/Overlay";
import "./GetReadyOverlay.css";
import orangeImg from "./orange1.svg";
const ANIMATION_DURATION_STEP_ONE = 16000;

export const GetReadyOverlay = ({ isShown }: { isShown: boolean }) => {
  const textStepOne = "It's time to focus on your health";
  const textStepTwo = "Ready to collect some oranges";
  const [text, setText] = useState(textStepOne);

  setTimeout(() => setText(textStepTwo), ANIMATION_DURATION_STEP_ONE);

  return (
    <Overlay>
      <div className="overlayContent">
        <img className="orange" src={orangeImg} alt="orange" />
        <div className="countdownText">{text}</div>
        <img className="orange" src={orangeImg} alt="orange" />
      </div>
    </Overlay>
  );
};
