import "./GetReadyOverlay.css";
import orangeImg from "./orange1.svg";

export const GetReadyOverlay = ({ text }: { text: string }) => {
  return (
    <div className="overlayContent">
      <img className="orange" src={orangeImg} alt="orange" />
      <div className="countdownText">{text}</div>
      <img className="orange" src={orangeImg} alt="orange" />
    </div>
  );
};
