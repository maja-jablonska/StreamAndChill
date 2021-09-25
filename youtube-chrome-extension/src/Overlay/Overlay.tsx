import { PropsWithChildren, ReactNode } from "react";

import "./Overlay.css";

export const Overlay = ({ children }: PropsWithChildren<ReactNode>) => (
  <div className="overlayContainer">{children}</div>
);
