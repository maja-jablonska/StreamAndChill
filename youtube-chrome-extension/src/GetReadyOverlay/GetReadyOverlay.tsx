import { Overlay } from "../Overlay/Overlay";
import "./GetReadyOverlay.css";
import orangeImg from "./orange1.svg";

export const GetReadyOverlay = ({ text }: { text: string }) => {
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
