import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, F} from './theme';

export const Scene: React.FC<{
  children: React.ReactNode;
  fadeOutFrom?: number;
}> = ({children, fadeOutFrom}) => {
  const frame = useCurrentFrame();
  const fadeIn = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const fadeOut =
    fadeOutFrom === undefined
      ? 1
      : interpolate(frame, [fadeOutFrom, fadeOutFrom + 15], [1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundColor: C.white,
        opacity: fadeIn * fadeOut,
        fontFamily: F.sans,
        color: C.ink,
        overflow: 'hidden',
      }}
    >
      {children}
    </div>
  );
};

export const FadeUp: React.FC<{
  delay?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({delay = 0, children, style}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - delay, fps, config: {damping: 200}});
  return (
    <div
      style={{
        opacity: s,
        transform: `translateY(${interpolate(s, [0, 1], [40, 0])}px)`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

export const Eyebrow: React.FC<{children: React.ReactNode}> = ({children}) => (
  <div
    style={{
      fontFamily: F.sans,
      fontSize: 24,
      letterSpacing: 8,
      textTransform: 'uppercase',
      color: C.gold,
      fontWeight: 600,
      marginBottom: 24,
    }}
  >
    {children}
  </div>
);

export const Headline: React.FC<{
  children: React.ReactNode;
  size?: number;
}> = ({children, size = 68}) => (
  <div
    style={{
      fontFamily: F.serif,
      fontSize: size,
      lineHeight: 1.15,
      color: C.ink,
      maxWidth: 1400,
    }}
  >
    {children}
  </div>
);

export const Caption: React.FC<{
  children: React.ReactNode;
  size?: number;
}> = ({children, size = 30}) => (
  <div
    style={{
      fontFamily: F.sans,
      fontSize: size,
      lineHeight: 1.5,
      color: C.muted,
      maxWidth: 1300,
    }}
  >
    {children}
  </div>
);

export const GoldRule: React.FC<{width?: number}> = ({width = 120}) => (
  <div
    style={{
      width,
      height: 4,
      backgroundColor: C.gold,
      margin: '28px 0',
    }}
  />
);

// A stylized purchase-order document card.
export const PODoc: React.FC<{
  label?: string;
  stamp?: {text: string; color: string; opacity?: number};
  width?: number;
  style?: React.CSSProperties;
}> = ({label = 'PURCHASE ORDER', stamp, width = 300, style}) => {
  const h = width * 1.28;
  return (
    <div
      style={{
        width,
        height: h,
        backgroundColor: '#FFFFFF',
        border: `1px solid #DDD5C4`,
        boxShadow: '0 18px 50px rgba(28,26,23,0.14)',
        padding: width * 0.09,
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        ...style,
      }}
    >
      <div
        style={{
          fontFamily: F.sans,
          fontWeight: 700,
          letterSpacing: 3,
          fontSize: width * 0.055,
          color: C.ink,
          borderBottom: `3px solid ${C.gold}`,
          paddingBottom: width * 0.045,
          marginBottom: width * 0.07,
        }}
      >
        {label}
      </div>
      {[0.9, 0.7, 0.82, 0.6, 0.75].map((w, i) => (
        <div
          key={i}
          style={{
            height: width * 0.032,
            width: `${w * 100}%`,
            backgroundColor: i === 0 ? C.goldTint : '#EDE8DD',
            marginBottom: width * 0.05,
          }}
        />
      ))}
      <div style={{flex: 1}} />
      <div
        style={{
          fontFamily: F.serif,
          fontStyle: 'italic',
          fontSize: width * 0.05,
          color: C.muted,
        }}
      >
        Signed &amp; legally contracted
      </div>
      {stamp ? (
        <div
          style={{
            position: 'absolute',
            top: '38%',
            left: '50%',
            transform: 'translate(-50%, -50%) rotate(-12deg)',
            border: `5px solid ${stamp.color}`,
            color: stamp.color,
            fontFamily: F.sans,
            fontWeight: 800,
            letterSpacing: 4,
            fontSize: width * 0.1,
            padding: `${width * 0.03}px ${width * 0.06}px`,
            opacity: stamp.opacity ?? 1,
            whiteSpace: 'nowrap',
          }}
        >
          {stamp.text}
        </div>
      ) : null}
    </div>
  );
};

export const Wordmark: React.FC<{size?: number; color?: string}> = ({
  size = 54,
  color = C.ink,
}) => (
  <div
    style={{
      fontFamily: F.serif,
      fontSize: size,
      letterSpacing: size * 0.35,
      color,
      fontWeight: 400,
    }}
  >
    TOTEM
  </div>
);
