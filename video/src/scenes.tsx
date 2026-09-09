import React from 'react';
import {
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {C, F} from './theme';
import {
  Caption,
  Eyebrow,
  FadeUp,
  GoldRule,
  Headline,
  PODoc,
  Scene,
  Wordmark,
} from './ui';

// Required by the Totem compliance manual: spoken/displayed at the open of any
// video for at least 5 seconds. Exact wording; do not paraphrase.
export const DisclaimerOpen: React.FC = () => {
  return (
    <Scene fadeOutFrom={165}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: 160,
        }}
      >
        <FadeUp>
          <Wordmark size={44} />
        </FadeUp>
        <FadeUp delay={8}>
          <div
            style={{
              width: 90,
              height: 3,
              backgroundColor: C.gold,
              margin: '48px auto',
            }}
          />
        </FadeUp>
        <FadeUp delay={14}>
          <div
            style={{
              fontFamily: F.sans,
              fontSize: 34,
              lineHeight: 1.65,
              color: C.ink,
              maxWidth: 1250,
            }}
          >
            Participation in commercial transactions involves risk, including
            possible loss of capital. Historical performance does not guarantee
            future outcomes.
          </div>
        </FadeUp>
      </div>
    </Scene>
  );
};

// Scene 1: a large institutional buyer submits a legally contracted PO.
export const SceneOrder: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const travel = spring({frame: frame - 55, fps, config: {damping: 200}, durationInFrames: 70});
  const poX = interpolate(travel, [0, 1], [-420, 420]);
  return (
    <Scene fadeOutFrom={285}>
      <div style={{position: 'absolute', top: 110, left: 140}}>
        <FadeUp>
          <Eyebrow>Where it starts</Eyebrow>
        </FadeUp>
        <FadeUp delay={6}>
          <Headline>
            A legally contracted <span style={{color: C.goldDeep}}>purchase order.</span>
          </Headline>
        </FadeUp>
        <FadeUp delay={14}>
          <div style={{marginTop: 26}}>
            <Caption>
              A large institutional buyer, like Amazon, submits a signed
              purchase order to its vendor.
            </Caption>
          </div>
        </FadeUp>
      </div>

      <div
        style={{
          position: 'absolute',
          bottom: 130,
          left: 0,
          right: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 340,
        }}
      >
        <FadeUp delay={20}>
          <div
            style={{
              width: 380,
              height: 220,
              backgroundColor: C.ink,
              color: C.white,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 14,
              boxShadow: '0 18px 50px rgba(28,26,23,0.25)',
            }}
          >
            <div style={{fontFamily: F.sans, fontWeight: 800, fontSize: 46, letterSpacing: 6}}>
              AMAZON
            </div>
            <div style={{fontFamily: F.sans, fontSize: 20, letterSpacing: 3, color: C.goldTint}}>
              INSTITUTIONAL BUYER
            </div>
          </div>
        </FadeUp>
        <FadeUp delay={28}>
          <div
            style={{
              width: 380,
              height: 220,
              backgroundColor: '#FFFFFF',
              border: `2px solid ${C.gold}`,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 14,
              boxShadow: '0 18px 50px rgba(28,26,23,0.12)',
            }}
          >
            <div style={{fontFamily: F.sans, fontWeight: 800, fontSize: 46, letterSpacing: 6}}>
              THE VENDOR
            </div>
            <div style={{fontFamily: F.sans, fontSize: 20, letterSpacing: 3, color: C.goldDeep}}>
              FULFILLS THE ORDER
            </div>
          </div>
        </FadeUp>
      </div>

      <div
        style={{
          position: 'absolute',
          bottom: 250,
          left: '50%',
          transform: `translateX(-50%) translateX(${poX}px) scale(0.62)`,
          opacity: interpolate(frame, [50, 62], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        <PODoc />
      </div>
    </Scene>
  );
};

// Scene 2: vendor capital already deployed across active POs.
export const SceneSqueeze: React.FC = () => {
  const frame = useCurrentFrame();
  const pulse = 0.55 + 0.45 * Math.abs(Math.sin(frame / 14));
  return (
    <Scene fadeOutFrom={285}>
      <div style={{position: 'absolute', top: 110, left: 140}}>
        <FadeUp>
          <Eyebrow>The squeeze</Eyebrow>
        </FadeUp>
        <FadeUp delay={6}>
          <Headline>
            His capital is <span style={{color: C.goldDeep}}>already deployed.</span>
          </Headline>
        </FadeUp>
        <FadeUp delay={14}>
          <div style={{marginTop: 26}}>
            <Caption>
              Multiple purchase orders are already in motion. The vendor cannot
              fund this new one, and the order will not wait.
            </Caption>
          </div>
        </FadeUp>
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: 120,
          left: 0,
          right: 0,
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'center',
          gap: 70,
        }}
      >
        {['PO No. 1', 'PO No. 2', 'PO No. 3'].map((label, i) => (
          <FadeUp key={label} delay={24 + i * 10}>
            <PODoc
              width={260}
              label={label}
              stamp={{text: 'CAPITAL IN', color: C.goldDeep, opacity: 0.85}}
            />
          </FadeUp>
        ))}
        <FadeUp delay={64}>
          <div style={{transform: 'scale(1.12)', transformOrigin: 'bottom center'}}>
            <PODoc
              width={280}
              label="NEW PO"
              stamp={{text: 'UNFUNDED', color: C.red, opacity: pulse}}
            />
          </div>
        </FadeUp>
      </div>
    </Scene>
  );
};

// Scene 3: the vendor messages Totem.
export const SceneMessage: React.FC = () => {
  return (
    <Scene fadeOutFrom={315}>
      <div style={{position: 'absolute', top: 110, left: 140}}>
        <FadeUp>
          <Eyebrow>The message</Eyebrow>
        </FadeUp>
        <FadeUp delay={6}>
          <Headline>
            This is where <span style={{color: C.goldDeep}}>Totem begins.</span>
          </Headline>
        </FadeUp>
      </div>
      <div
        style={{
          position: 'absolute',
          top: 400,
          left: 0,
          right: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 44,
        }}
      >
        <FadeUp delay={30}>
          <div
            style={{
              maxWidth: 1050,
              backgroundColor: '#FFFFFF',
              border: '1px solid #DDD5C4',
              borderRadius: '28px 28px 28px 6px',
              padding: '44px 56px',
              fontFamily: F.sans,
              fontSize: 36,
              lineHeight: 1.5,
              boxShadow: '0 18px 50px rgba(28,26,23,0.12)',
            }}
          >
            <div
              style={{
                fontSize: 20,
                letterSpacing: 3,
                color: C.muted,
                marginBottom: 16,
                fontWeight: 700,
              }}
            >
              THE VENDOR
            </div>
            “I have a signed purchase order from a Fortune 100 buyer. My capital
            is committed across three active orders. Can Totem fund this one?”
          </div>
        </FadeUp>
        <FadeUp delay={95}>
          <div
            style={{
              maxWidth: 900,
              backgroundColor: C.ink,
              color: C.white,
              borderRadius: '28px 28px 6px 28px',
              padding: '44px 56px',
              fontFamily: F.sans,
              fontSize: 36,
              lineHeight: 1.5,
              boxShadow: '0 18px 50px rgba(28,26,23,0.25)',
              alignSelf: 'flex-end',
              marginLeft: 500,
            }}
          >
            <div
              style={{
                fontSize: 20,
                letterSpacing: 3,
                color: C.gold,
                marginBottom: 16,
                fontWeight: 700,
              }}
            >
              TOTEM
            </div>
            “Send it over. Our business starts exactly here.”
          </div>
        </FadeUp>
      </div>
    </Scene>
  );
};

// Scene 4: member capital funds the PO.
export const SceneFunding: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const members = [0, 1, 2, 3, 4, 5];
  const stampIn = spring({frame: frame - 150, fps, config: {damping: 14}});
  return (
    <Scene fadeOutFrom={315}>
      <div style={{position: 'absolute', top: 110, left: 140}}>
        <FadeUp>
          <Eyebrow>The funding</Eyebrow>
        </FadeUp>
        <FadeUp delay={6}>
          <Headline>
            Totem brings the capital, <span style={{color: C.goldDeep}}>through its members.</span>
          </Headline>
        </FadeUp>
        <FadeUp delay={14}>
          <div style={{marginTop: 26}}>
            <Caption>
              These are purchase orders of necessity: orders a business needs to
              keep its operations running.
            </Caption>
          </div>
        </FadeUp>
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: 110,
          left: 0,
          right: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 220,
        }}
      >
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 40}}>
          {members.map((m) => (
            <FadeUp key={m} delay={24 + m * 8}>
              <div
                style={{
                  width: 150,
                  height: 150,
                  borderRadius: '50%',
                  backgroundColor: C.goldTint,
                  border: `2px solid ${C.gold}`,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontFamily: F.sans,
                }}
              >
                <div style={{fontSize: 40, color: C.goldDeep, fontWeight: 700}}>
                  ●
                </div>
                <div style={{fontSize: 17, letterSpacing: 2, color: C.goldDeep, fontWeight: 700}}>
                  MEMBER
                </div>
              </div>
            </FadeUp>
          ))}
        </div>
        <div style={{position: 'relative'}}>
          {/* Capital flow dots traveling toward the PO */}
          {members.map((m) => {
            const t = ((frame * 2 + m * 34) % 100) / 100;
            const opacity = frame > 80 && frame < 170 ? interpolate(t, [0, 0.1, 0.9, 1], [0, 1, 1, 0]) : 0;
            return (
              <div
                key={m}
                style={{
                  position: 'absolute',
                  left: interpolate(t, [0, 1], [-190, -20]),
                  top: 60 + m * 55,
                  width: 16,
                  height: 16,
                  borderRadius: '50%',
                  backgroundColor: C.gold,
                  opacity,
                }}
              />
            );
          })}
          <PODoc width={320} />
          <div
            style={{
              position: 'absolute',
              top: '42%',
              left: '50%',
              transform: `translate(-50%, -50%) rotate(-12deg) scale(${stampIn})`,
              border: `6px solid ${C.goldDeep}`,
              color: C.goldDeep,
              fontFamily: F.sans,
              fontWeight: 800,
              letterSpacing: 4,
              fontSize: 34,
              padding: '12px 26px',
              backgroundColor: 'rgba(250,248,244,0.9)',
              whiteSpace: 'nowrap',
            }}
          >
            FUNDED
          </div>
        </div>
      </div>
    </Scene>
  );
};

const Stat: React.FC<{
  big: string;
  label: string;
  delay: number;
}> = ({big, label, delay}) => (
  <FadeUp delay={delay}>
    <div
      style={{
        width: 380,
        height: 300,
        backgroundColor: '#FFFFFF',
        border: '1px solid #DDD5C4',
        borderTop: `6px solid ${C.gold}`,
        boxShadow: '0 18px 50px rgba(28,26,23,0.10)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        padding: '0 36px',
        gap: 22,
      }}
    >
      <div style={{fontFamily: F.serif, fontSize: 76, color: C.goldDeep}}>{big}</div>
      <div style={{fontFamily: F.sans, fontSize: 24, lineHeight: 1.45, color: C.ink}}>
        {label}
      </div>
    </div>
  </FadeUp>
);

// Scene 5: the member terms, with the mandatory insurance disclaimer inline.
export const SceneTerms: React.FC = () => {
  return (
    <Scene fadeOutFrom={435}>
      <div style={{position: 'absolute', top: 90, left: 0, right: 0, textAlign: 'center'}}>
        <FadeUp>
          <div style={{display: 'flex', justifyContent: 'center'}}>
            <Eyebrow>The structure for members</Eyebrow>
          </div>
        </FadeUp>
      </div>
      <div
        style={{
          position: 'absolute',
          top: 190,
          left: 0,
          right: 0,
          display: 'flex',
          justifyContent: 'center',
          gap: 44,
        }}
      >
        <Stat big="5%" label="Fixed origination fee, defined per agreement" delay={12} />
        <Stat big="90 days" label="Fixed transaction cycle with a defined capital return event" delay={24} />
        <Stat big="Built in" label="Insurance is structured into the transaction itself" delay={36} />
        <Stat big="A-rated" label="Global insurance carrier arrangement at the transaction level" delay={48} />
      </div>
      <div
        style={{
          position: 'absolute',
          top: 560,
          left: 0,
          right: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          gap: 30,
          padding: '0 200px',
        }}
      >
        <FadeUp delay={70}>
          <div
            style={{
              fontFamily: F.serif,
              fontSize: 40,
              lineHeight: 1.4,
              color: C.ink,
              maxWidth: 1350,
            }}
          >
            Members do not purchase a separate personal policy. Coverage is
            arranged inside the transaction from day one.
          </div>
        </FadeUp>
        <FadeUp delay={95}>
          <div
            style={{
              fontFamily: F.sans,
              fontSize: 21,
              lineHeight: 1.6,
              color: C.muted,
              maxWidth: 1500,
              borderTop: '1px solid #DDD5C4',
              paddingTop: 26,
            }}
          >
            Insurance arrangements, where applicable, are subject to carrier
            approval, policy terms, exclusions, limitations, claims processes,
            and carrier performance and do not guarantee transaction performance
            or repayment.
          </div>
        </FadeUp>
      </div>
    </Scene>
  );
};

// Scene 6: close.
export const SceneClose: React.FC = () => {
  return (
    <Scene>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '0 160px',
        }}
      >
        <FadeUp>
          <Wordmark size={92} />
        </FadeUp>
        <FadeUp delay={12}>
          <div style={{display: 'flex', justifyContent: 'center'}}>
            <GoldRule width={160} />
          </div>
        </FadeUp>
        <FadeUp delay={18}>
          <div style={{fontFamily: F.serif, fontStyle: 'italic', fontSize: 44, color: C.goldDeep}}>
            Capital for purchase orders of necessity.
          </div>
        </FadeUp>
        <FadeUp delay={40}>
          <div
            style={{
              position: 'absolute',
              bottom: -280,
              left: '50%',
              transform: 'translateX(-50%)',
              width: 1500,
              fontFamily: F.sans,
              fontSize: 19,
              lineHeight: 1.6,
              color: C.muted,
            }}
          >
            This material is provided for informational purposes only and does
            not constitute legal, tax, securities, lending, investment, or
            financial advice. Participation in commercial transactions involves
            risk, including possible loss of capital. Historical performance
            does not guarantee future outcomes.
          </div>
        </FadeUp>
      </div>
    </Scene>
  );
};
