import orangeImg from "../assets/orange3.svg";
import "./BreathingAnimation.scss";

export const BreathingAnimation = () => {
  return (
    <div className="breathingAnimation">
      <div className="breathingText">
        <span className="breathIn"></span>
        <span className="breathOut"></span>
      </div>
      <div className="breathingOrange">
        <img src={orangeImg} alt="orange" />
      </div>
    </div>
  );
};
