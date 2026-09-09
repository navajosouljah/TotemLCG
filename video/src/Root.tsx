import React from 'react';
import {Composition, Series} from 'remotion';
import {
  DisclaimerOpen,
  SceneClose,
  SceneFunding,
  SceneMessage,
  SceneOrder,
  SceneSqueeze,
  SceneTerms,
} from './scenes';

const DURATIONS = {
  disclaimer: 180, // 6s: manual requires >= 5s on screen
  order: 300,
  squeeze: 300,
  message: 330,
  funding: 330,
  terms: 450,
  close: 240,
};

export const TotemVideo: React.FC = () => (
  <Series>
    <Series.Sequence durationInFrames={DURATIONS.disclaimer}>
      <DisclaimerOpen />
    </Series.Sequence>
    <Series.Sequence durationInFrames={DURATIONS.order}>
      <SceneOrder />
    </Series.Sequence>
    <Series.Sequence durationInFrames={DURATIONS.squeeze}>
      <SceneSqueeze />
    </Series.Sequence>
    <Series.Sequence durationInFrames={DURATIONS.message}>
      <SceneMessage />
    </Series.Sequence>
    <Series.Sequence durationInFrames={DURATIONS.funding}>
      <SceneFunding />
    </Series.Sequence>
    <Series.Sequence durationInFrames={DURATIONS.terms}>
      <SceneTerms />
    </Series.Sequence>
    <Series.Sequence durationInFrames={DURATIONS.close}>
      <SceneClose />
    </Series.Sequence>
  </Series>
);

const TOTAL = Object.values(DURATIONS).reduce((a, b) => a + b, 0);

export const RemotionRoot: React.FC = () => (
  <Composition
    id="TotemVendorFinancing"
    component={TotemVideo}
    durationInFrames={TOTAL}
    fps={30}
    width={1920}
    height={1080}
  />
);
