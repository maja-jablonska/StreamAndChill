import "./ConfettiCelebration.css";
import meditationImg from "../assets/meditation.png";
import { useState } from "react";

export const ConfettiCelebration = () => {
  const [text, setText] = useState("");
  return (
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
        <img
          src={meditationImg}
          alt="meditation"
          onLoad={() => setText("You earned 2 oranges 🍊 Awesome!")}
        />
        <p>{text}</p>
      </div>
    </>
  );
};
