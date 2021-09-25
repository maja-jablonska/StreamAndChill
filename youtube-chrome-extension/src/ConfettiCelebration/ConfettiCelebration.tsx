import "./ConfettiCelebration.css";
import meditationImg from "../assets/meditation.png";

export const ConfettiCelebration = () => (
  <>
    <div className="confetti">
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
      <div className="confetti-piece"></div>
    </div>
    <div className="meditationAndText">
      <img src={meditationImg} alt="meditation" />
      <p>You earned 2 oranges 🍊 Awesome!</p>
    </div>
  </>
);
