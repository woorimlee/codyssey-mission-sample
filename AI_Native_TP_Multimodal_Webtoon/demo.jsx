import { useState, useEffect, useRef } from "react";

const SAMPLE_STORY = {
  title: "숲속의 기사 토끼",
  genre: "판타지 동화",
  character: "흰 털에 은색 갑옷, 파란 망토를 두른 토끼 기사 '달'",
  plot: "어두운 안개가 숲을 뒤덮자, 용감한 토끼 기사 달이 숲의 빛을 되찾기 위해 모험을 떠난다",
  style: "watercolor",
  scenes: [
    {
      id: 1,
      title: "숲 입구의 기사",
      narration: "옛날 옛적, 햇살 가득한 숲 입구에 용감한 토끼 기사 '달'이 살았습니다.\n작은 나무 검을 꼭 쥐고, 파란 망토를 펄럭이며 매일 숲을 지켰지요.",
      imagePrompt: "A cute small white rabbit with round bright eyes and pink inner ears. Wearing a polished silver chest plate armor with a small golden crest on the front, a round silver helmet with two holes for his long ears poking through, a flowing royal blue cape fastened with a gold clasp at the neck, and carrying a hand-carved wooden sword with leather grip and a tiny star engraved on the crossguard. The rabbit stands heroically at the entrance of a bright sunlit forest, one paw on his hip, the other resting the wooden sword on his shoulder. His cape drapes gently in the breeze. Behind him, tall friendly trees and a field of colorful wildflowers. Morning golden light filters through the canopy, casting dappled shadows on his shining armor. Children's book illustration, soft watercolor style, warm pastel colors, gentle brushstrokes, storybook aesthetic, no text.",
      imageUrl: "/sample_images/scene01_forest_entrance.png",
      bgColor: "#FFF8E7",
    },
    {
      id: 2,
      title: "어두운 안개",
      narration: "그런데 어느 날, 숲에 보라색 안개가 피어올랐습니다.\n나무들이 시들고, 동물 친구들이 하나둘 사라졌어요.\n\"내가 가서 안개를 물리칠 거야!\" 달은 떨리는 마음을 꾹 누르고 안개 속으로 들어갔습니다.",
      imagePrompt: "A cute small white rabbit with round bright eyes and pink inner ears. Wearing a polished silver chest plate armor with a small golden crest on the front, a round silver helmet with two holes for his long ears poking through, a flowing royal blue cape fastened with a gold clasp at the neck, and carrying a hand-carved wooden sword with leather grip and a tiny star engraved on the crossguard. The rabbit marches forward with one foot stepping into thick purple fog, his royal blue cape billowing behind him in the wind. His sword arm is raised slightly, the tiny star on the crossguard casting a faint warm golden glow that cuts through the darkness. His silver armor reflects hints of purple mist light. Twisted dark trees lean inward from both sides like a tunnel. Low angle shot from behind, showing the rabbit's small determined silhouette against the vast dark forest ahead. Children's book illustration, soft watercolor style, warm pastel colors mixed with mysterious purple tones, gentle brushstrokes, storybook aesthetic, sense of motion and bravery, no text.",
      imageUrl: "/sample_images/scene02_dark_mist.png",
      bgColor: "#F0E8F5",
    },
    {
      id: 3,
      title: "안개의 왕",
      narration: "숲 한가운데, 거대한 안개 그림자가 나타났습니다.\n\"이 숲은 이제 내 것이다!\" 안개의 왕이 으르렁댔지요.\n하지만 달은 나무 검을 높이 들었습니다. 검에서 따뜻한 금빛이 퍼져나갔어요!",
      imagePrompt: "A cute small white rabbit with round bright eyes and pink inner ears. Wearing a polished silver chest plate armor with a small golden crest on the front, a round silver helmet with two holes for his long ears poking through, a flowing royal blue cape fastened with a gold clasp at the neck, and carrying a hand-carved wooden sword with leather grip and a tiny star engraved on the crossguard. The rabbit holds the wooden sword high above his head with both paws. The tiny star on the crossguard erupts with brilliant warm golden light, radiating outward like a small sun. His silver armor glows from the reflected light, the golden crest shining bright. His blue cape spreads wide behind him like wings. He faces a towering shadowy purple mist creature, the Fog King, made of swirling dark clouds with piercing glowing yellow eyes. Epic confrontation in the heart of the forest. Children's book illustration, soft watercolor style, dramatic contrast between warm golden light and dark purple shadows, gentle brushstrokes, storybook aesthetic, no text.",
      imageUrl: "/sample_images/scene03_confrontation.png",
      bgColor: "#EDE3F5",
    },
    {
      id: 4,
      title: "빛이 돌아온 숲",
      narration: "금빛이 안개를 모두 걷어냈습니다!\n숲에 다시 햇살이 내리쬐고, 꽃이 활짝 피어났지요.\n동물 친구들이 달을 둘러싸고 환호했습니다.\n\"고마워, 달! 넌 진짜 용감한 기사야!\"",
      imagePrompt: "A cute small white rabbit with round bright eyes and pink inner ears. Wearing a polished silver chest plate armor with a small golden crest on the front, a round silver helmet slightly tilted back showing his happy face, two long ears poking through the helmet holes and flopping relaxed, a royal blue cape with gold clasp resting softly on his shoulders, and the hand-carved wooden sword with leather grip and tiny star on the crossguard tucked casually at his side. The rabbit smiles warmly, surrounded by cute woodland animals — a small fox, a spotted deer, a round owl, and a fluffy squirrel — all celebrating together. The forest is bright and peaceful with golden sunlight streaming through the trees. Flowers bloom everywhere in soft pinks, yellows, and whites. His armor has a few small dents and scratches from the adventure, adding character. Children's book illustration, soft watercolor style, warm pastel colors, joyful peaceful atmosphere, gentle brushstrokes, storybook aesthetic, no text.",
      imageUrl: "/sample_images/scene04_happy_ending.png",
      bgColor: "#FFF5E6",
    },
  ],
};

const CONSISTENCY_CHECKS = [
  { item: "털 색상", key: "fur" },
  { item: "은색 갑옷", key: "armor" },
  { item: "파란 망토", key: "cape" },
  { item: "나무 검", key: "sword" },
  { item: "분홍 귀 안쪽", key: "ears" },
  { item: "둥근 밝은 눈", key: "eyes" },
  { item: "수채화풍", key: "style" },
  { item: "파스텔 색감", key: "palette" },
];

const SAMPLE_REPORT = [
  { scene: 1, fur: true, armor: true, cape: true, sword: true, ears: true, eyes: true, style: true, palette: true },
  { scene: 2, fur: true, armor: true, cape: true, sword: true, ears: false, eyes: true, style: true, palette: true },
  { scene: 3, fur: true, armor: true, cape: false, sword: true, ears: true, eyes: true, style: true, palette: true },
  { scene: 4, fur: true, armor: true, cape: true, sword: true, ears: true, eyes: true, style: true, palette: true },
];

// Watercolor-style SVG placeholder
function PlaceholderImage({ scene, size = 320 }) {
  const colors = {
    1: { bg: "#FFF3D4", accent: "#7CB342", detail: "#FFB74D" },
    2: { bg: "#E8D5F0", accent: "#7E57C2", detail: "#90A4AE" },
    3: { bg: "#E0D0F0", accent: "#FF8A65", detail: "#5C6BC0" },
    4: { bg: "#FFF8E1", accent: "#66BB6A", detail: "#FFD54F" },
  };
  const c = colors[scene.id] || colors[1];
  
  return (
    <div style={{
      width: "100%",
      aspectRatio: "4/3",
      background: `linear-gradient(135deg, ${c.bg}, ${c.accent}22)`,
      borderRadius: 16,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      gap: 8,
      border: `2px dashed ${c.accent}66`,
      position: "relative",
      overflow: "hidden",
    }}>
      <div style={{ fontSize: 56, filter: "grayscale(0.3)" }}>
        {scene.id === 1 ? "🐰⚔️🌳" : scene.id === 2 ? "🐰🌫️🌑" : scene.id === 3 ? "🐰✨👾" : "🐰🎉🌸"}
      </div>
      <div style={{ fontSize: 13, color: c.accent, fontWeight: 600, letterSpacing: 1 }}>
        SCENE {scene.id}
      </div>
      <div style={{ fontSize: 11, color: "#999", maxWidth: "80%", textAlign: "center" }}>
        Gemini로 이미지 생성 후 교체
      </div>
    </div>
  );
}

function SceneImage({ scene }) {
  if (scene.imageUrl) {
    return (
      <img
        src={scene.imageUrl}
        alt={scene.title}
        style={{
          width: "100%",
          aspectRatio: "4/3",
          objectFit: "cover",
          borderRadius: 16,
          boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
        }}
      />
    );
  }
  return <PlaceholderImage scene={scene} />;
}

// Agent log animation
function AgentLog({ logs, isGenerating }) {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current) ref.current.scrollTop = ref.current.scrollHeight;
  }, [logs]);

  return (
    <div
      ref={ref}
      style={{
        background: "#1a1a2e",
        borderRadius: 12,
        padding: 20,
        fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
        fontSize: 13,
        lineHeight: 1.8,
        maxHeight: 360,
        overflowY: "auto",
        color: "#a0a0b0",
      }}
    >
      {logs.map((log, i) => (
        <div key={i} style={{ marginBottom: 4 }}>
          {log.type === "writer" && (
            <span><span style={{ color: "#7CB342" }}>{"[Writer Agent]"}</span> {log.text}</span>
          )}
          {log.type === "illustrator" && (
            <span><span style={{ color: "#42A5F5" }}>{"[Illustrator Agent]"}</span> {log.text}</span>
          )}
          {log.type === "system" && (
            <span style={{ color: "#FF8A65" }}>{log.text}</span>
          )}
          {log.type === "safety" && (
            <span><span style={{ color: "#EF5350" }}>{"[Safety Check]"}</span> {log.text}</span>
          )}
        </div>
      ))}
      {isGenerating && (
        <span style={{ color: "#FFD54F" }}>
          {"▊"}
        </span>
      )}
    </div>
  );
}

// Storybook viewer
function StorybookViewer({ story }) {
  const [currentPage, setCurrentPage] = useState(0);
  const scene = story.scenes[currentPage];

  return (
    <div style={{
      background: scene.bgColor,
      borderRadius: 24,
      padding: 32,
      transition: "background 0.6s ease",
      minHeight: 500,
    }}>
      {/* Page indicator */}
      <div style={{ display: "flex", justifyContent: "center", gap: 8, marginBottom: 24 }}>
        {story.scenes.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrentPage(i)}
            style={{
              width: i === currentPage ? 32 : 10,
              height: 10,
              borderRadius: 5,
              border: "none",
              background: i === currentPage ? "#7E57C2" : "#D1C4E9",
              cursor: "pointer",
              transition: "all 0.3s ease",
            }}
          />
        ))}
      </div>

      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 32,
        alignItems: "center",
      }}>
        {/* Image */}
        <div>
          <SceneImage scene={scene} />
        </div>

        {/* Text */}
        <div>
          <div style={{
            fontSize: 12,
            color: "#7E57C2",
            fontWeight: 700,
            letterSpacing: 2,
            marginBottom: 8,
          }}>
            SCENE {scene.id}
          </div>
          <h3 style={{
            fontFamily: "'Noto Serif KR', Georgia, serif",
            fontSize: 24,
            fontWeight: 700,
            color: "#2D2D3F",
            marginBottom: 16,
            margin: 0,
            marginTop: 0,
          }}>
            {scene.title}
          </h3>
          <p style={{
            fontFamily: "'Noto Serif KR', Georgia, serif",
            fontSize: 16,
            lineHeight: 2,
            color: "#4A4A5A",
            whiteSpace: "pre-line",
            margin: 0,
            marginTop: 16,
          }}>
            {scene.narration}
          </p>
        </div>
      </div>

      {/* Navigation */}
      <div style={{ display: "flex", justifyContent: "space-between", marginTop: 32 }}>
        <button
          onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
          disabled={currentPage === 0}
          style={{
            padding: "10px 24px",
            borderRadius: 20,
            border: "none",
            background: currentPage === 0 ? "#E0E0E0" : "#7E57C2",
            color: currentPage === 0 ? "#999" : "white",
            cursor: currentPage === 0 ? "default" : "pointer",
            fontSize: 14,
            fontWeight: 600,
          }}
        >
          ← 이전
        </button>
        <span style={{ color: "#999", fontSize: 14, alignSelf: "center" }}>
          {currentPage + 1} / {story.scenes.length}
        </span>
        <button
          onClick={() => setCurrentPage(Math.min(story.scenes.length - 1, currentPage + 1))}
          disabled={currentPage === story.scenes.length - 1}
          style={{
            padding: "10px 24px",
            borderRadius: 20,
            border: "none",
            background: currentPage === story.scenes.length - 1 ? "#E0E0E0" : "#7E57C2",
            color: currentPage === story.scenes.length - 1 ? "#999" : "white",
            cursor: currentPage === story.scenes.length - 1 ? "default" : "pointer",
            fontSize: 14,
            fontWeight: 600,
          }}
        >
          다음 →
        </button>
      </div>
    </div>
  );
}

// Consistency Report
function ConsistencyReport({ story }) {
  const totalChecks = SAMPLE_REPORT.length * CONSISTENCY_CHECKS.length;
  const passedChecks = SAMPLE_REPORT.reduce(
    (sum, row) => sum + CONSISTENCY_CHECKS.filter((c) => row[c.key]).length, 0
  );
  const score = Math.round((passedChecks / totalChecks) * 100);
  const failedScenes = SAMPLE_REPORT.filter(
    (row) => CONSISTENCY_CHECKS.some((c) => !row[c.key])
  );

  return (
    <div style={{ background: "white", borderRadius: 16, padding: 28, boxShadow: "0 2px 12px rgba(0,0,0,0.06)" }}>
      <h3 style={{ margin: 0, marginBottom: 20, color: "#2D2D3F", fontSize: 18 }}>
        일관성 테스트 리포트
      </h3>

      {/* Score */}
      <div style={{
        display: "flex",
        alignItems: "center",
        gap: 16,
        marginBottom: 24,
        padding: 16,
        background: score >= 90 ? "#E8F5E9" : score >= 70 ? "#FFF8E1" : "#FFEBEE",
        borderRadius: 12,
      }}>
        <div style={{
          width: 64,
          height: 64,
          borderRadius: "50%",
          background: score >= 90 ? "#4CAF50" : score >= 70 ? "#FF9800" : "#F44336",
          color: "white",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 22,
          fontWeight: 800,
        }}>
          {score}%
        </div>
        <div>
          <div style={{ fontWeight: 700, color: "#333" }}>
            {passedChecks}/{totalChecks} 항목 통과
          </div>
          <div style={{ fontSize: 13, color: "#666", marginTop: 4 }}>
            {failedScenes.length > 0
              ? `실패 컷: Scene ${failedScenes.map((r) => r.scene).join(", ")}`
              : "모든 씬에서 일관성 유지"}
          </div>
        </div>
      </div>

      {/* Table */}
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
          <thead>
            <tr style={{ background: "#F5F5F5" }}>
              <th style={{ padding: "10px 12px", textAlign: "left", borderBottom: "2px solid #E0E0E0" }}>씬</th>
              {CONSISTENCY_CHECKS.map((c) => (
                <th key={c.key} style={{ padding: "10px 8px", textAlign: "center", borderBottom: "2px solid #E0E0E0", fontSize: 12 }}>
                  {c.item}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {SAMPLE_REPORT.map((row) => (
              <tr key={row.scene} style={{ borderBottom: "1px solid #EEE" }}>
                <td style={{ padding: "10px 12px", fontWeight: 600 }}>Scene {row.scene}</td>
                {CONSISTENCY_CHECKS.map((c) => (
                  <td key={c.key} style={{ padding: "10px 8px", textAlign: "center" }}>
                    {row[c.key]
                      ? <span style={{ color: "#4CAF50", fontWeight: 700 }}>OK</span>
                      : <span style={{ color: "#F44336", fontWeight: 700 }}>FAIL</span>}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ marginTop: 16, padding: 12, background: "#FFF3E0", borderRadius: 8, fontSize: 13, color: "#E65100" }}>
        Scene 2: 안개가 짙어 귀 안쪽 분홍색이 보이지 않음 · Scene 3: 전투 장면에서 망토가 바람에 날려 색상 식별 어려움
      </div>
    </div>
  );
}

// Main App
export default function App() {
  const [tab, setTab] = useState("input");
  const [story, setStory] = useState(SAMPLE_STORY);
  const [genre, setGenre] = useState("판타지 동화");
  const [character, setCharacter] = useState("흰 털에 은색 갑옷, 파란 망토를 두른 토끼 기사 '달'");
  const [plot, setPlot] = useState("어두운 안개가 숲을 뒤덮자, 용감한 토끼 기사 달이 숲의 빛을 되찾기 위해 모험을 떠난다");
  const [artStyle, setArtStyle] = useState("watercolor");
  const [isGenerating, setIsGenerating] = useState(false);
  const [logs, setLogs] = useState([]);
  const [showPrompt, setShowPrompt] = useState(null);

  const addLog = (type, text, delay) =>
    new Promise((resolve) =>
      setTimeout(() => {
        setLogs((prev) => [...prev, { type, text }]);
        resolve();
      }, delay)
    );

  const simulateGeneration = async () => {
    setIsGenerating(true);
    setLogs([]);
    setTab("process");

    await addLog("system", "=== 멀티 에이전트 파이프라인 시작 ===", 300);
    await addLog("system", `장르: ${genre} | 화풍: ${artStyle}`, 400);
    await addLog("system", `주인공: ${character}`, 300);

    for (let i = 1; i <= 4; i++) {
      await addLog("writer", `장면 ${i} 분석 중...`, 800);
      await addLog("writer", `장면 ${i} 묘사 텍스트 생성 완료`, 600);
      await addLog("safety", `장면 ${i} 텍스트 유해성 검사... PASS ✓`, 400);
      await addLog("illustrator", `이미지 프롬프트 구성 (캐릭터 앵커 + 씬 묘사)`, 500);
      await addLog("illustrator", `이미지 생성 요청 (Style: ${artStyle})... 완료 ✓`, 900);
      await addLog("safety", `장면 ${i} 이미지 Safety Check... PASS ✓`, 400);
    }

    await addLog("system", "=== 일관성 테스트 실행 ===", 600);
    await addLog("system", "캐릭터 특징 8개 항목 × 4씬 = 32개 체크", 400);
    await addLog("system", "일관성 점수: 94% (30/32 통과)", 500);
    await addLog("system", "=== 생성 완료! 스토리북 뷰어로 이동합니다 ===", 400);

    setIsGenerating(false);
    setTimeout(() => setTab("viewer"), 800);
  };

  const tabs = [
    { id: "input", label: "스토리 입력", icon: "✏️" },
    { id: "process", label: "생성 과정", icon: "⚙️" },
    { id: "viewer", label: "스토리북", icon: "📖" },
    { id: "gallery", label: "갤러리", icon: "🖼️" },
    { id: "report", label: "일관성 리포트", icon: "📊" },
  ];

  return (
    <div style={{
      minHeight: "100vh",
      background: "#FAFAFA",
      fontFamily: "'Pretendard', 'Apple SD Gothic Neo', sans-serif",
    }}>
      {/* Header */}
      <header style={{
        background: "linear-gradient(135deg, #7E57C2, #5C6BC0)",
        padding: "20px 32px",
        color: "white",
      }}>
        <div style={{ maxWidth: 960, margin: "0 auto", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <h1 style={{ margin: 0, fontSize: 22, fontWeight: 800, letterSpacing: -0.5 }}>
              📚 AI 동화 창작소
            </h1>
            <p style={{ margin: 0, marginTop: 4, fontSize: 13, opacity: 0.8 }}>
              Writer + Illustrator 멀티 에이전트 플랫폼
            </p>
          </div>
          <div style={{ fontSize: 12, opacity: 0.7 }}>
            Term Project C · Demo
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <nav style={{
        maxWidth: 960,
        margin: "0 auto",
        display: "flex",
        gap: 4,
        padding: "16px 0 0",
      }}>
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            style={{
              padding: "10px 18px",
              borderRadius: "12px 12px 0 0",
              border: "none",
              background: tab === t.id ? "white" : "transparent",
              color: tab === t.id ? "#5C6BC0" : "#999",
              fontWeight: tab === t.id ? 700 : 500,
              fontSize: 14,
              cursor: "pointer",
              boxShadow: tab === t.id ? "0 -2px 8px rgba(0,0,0,0.06)" : "none",
              transition: "all 0.2s",
            }}
          >
            {t.icon} {t.label}
          </button>
        ))}
      </nav>

      {/* Content */}
      <main style={{
        maxWidth: 960,
        margin: "0 auto",
        background: "white",
        borderRadius: "0 16px 16px 16px",
        padding: 32,
        minHeight: 500,
        boxShadow: "0 2px 12px rgba(0,0,0,0.06)",
        marginBottom: 48,
      }}>

        {/* --- INPUT TAB --- */}
        {tab === "input" && (
          <div>
            <h2 style={{ margin: 0, marginBottom: 8, color: "#2D2D3F" }}>이야기를 들려주세요</h2>
            <p style={{ color: "#888", marginTop: 0, marginBottom: 28, fontSize: 14 }}>
              장르, 주인공, 줄거리를 입력하면 AI가 동화를 만들어줍니다.
            </p>

            <div style={{ display: "grid", gap: 20 }}>
              <div>
                <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#555", marginBottom: 6 }}>장르</label>
                <select
                  value={genre}
                  onChange={(e) => setGenre(e.target.value)}
                  style={{ width: "100%", padding: 12, borderRadius: 10, border: "1.5px solid #E0E0E0", fontSize: 15, background: "white" }}
                >
                  <option>판타지 동화</option>
                  <option>모험 이야기</option>
                  <option>우정 이야기</option>
                  <option>자연/동물 이야기</option>
                </select>
              </div>

              <div>
                <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#555", marginBottom: 6 }}>화풍 스타일</label>
                <div style={{ display: "flex", gap: 10 }}>
                  {[
                    { id: "watercolor", label: "수채화", emoji: "🎨" },
                    { id: "cartoon", label: "만화", emoji: "✏️" },
                    { id: "pixel", label: "픽셀아트", emoji: "👾" },
                  ].map((s) => (
                    <button
                      key={s.id}
                      onClick={() => setArtStyle(s.id)}
                      style={{
                        flex: 1,
                        padding: "14px 12px",
                        borderRadius: 12,
                        border: artStyle === s.id ? "2px solid #7E57C2" : "2px solid #E8E8E8",
                        background: artStyle === s.id ? "#F3E5F5" : "white",
                        cursor: "pointer",
                        fontSize: 14,
                        fontWeight: artStyle === s.id ? 700 : 400,
                        color: artStyle === s.id ? "#7E57C2" : "#666",
                      }}
                    >
                      {s.emoji} {s.label}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#555", marginBottom: 6 }}>주인공 특징</label>
                <input
                  value={character}
                  onChange={(e) => setCharacter(e.target.value)}
                  placeholder="예: 흰 털에 은색 갑옷을 입은 토끼 기사"
                  style={{ width: "100%", padding: 12, borderRadius: 10, border: "1.5px solid #E0E0E0", fontSize: 15, boxSizing: "border-box" }}
                />
              </div>

              <div>
                <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#555", marginBottom: 6 }}>줄거리 요약</label>
                <textarea
                  value={plot}
                  onChange={(e) => setPlot(e.target.value)}
                  rows={3}
                  placeholder="예: 어두운 안개가 숲을 뒤덮자, 용감한 토끼 기사가 모험을 떠난다"
                  style={{ width: "100%", padding: 12, borderRadius: 10, border: "1.5px solid #E0E0E0", fontSize: 15, resize: "vertical", boxSizing: "border-box" }}
                />
              </div>

              <button
                onClick={simulateGeneration}
                disabled={isGenerating}
                style={{
                  padding: "16px 32px",
                  borderRadius: 14,
                  border: "none",
                  background: "linear-gradient(135deg, #7E57C2, #5C6BC0)",
                  color: "white",
                  fontSize: 16,
                  fontWeight: 700,
                  cursor: isGenerating ? "wait" : "pointer",
                  opacity: isGenerating ? 0.7 : 1,
                  marginTop: 8,
                  letterSpacing: 0.5,
                }}
              >
                {isGenerating ? "생성 중..." : "✨ 동화 만들기"}
              </button>
            </div>
          </div>
        )}

        {/* --- PROCESS TAB --- */}
        {tab === "process" && (
          <div>
            <h2 style={{ margin: 0, marginBottom: 8, color: "#2D2D3F" }}>에이전트 생성 과정</h2>
            <p style={{ color: "#888", marginTop: 0, marginBottom: 20, fontSize: 14 }}>
              Writer → Safety Check → Illustrator → Safety Check 파이프라인
            </p>

            <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
              {["Writer Agent", "Safety Check", "Illustrator Agent"].map((name, i) => (
                <div
                  key={name}
                  style={{
                    flex: 1,
                    padding: "10px 14px",
                    borderRadius: 10,
                    background: ["#E8F5E9", "#FFEBEE", "#E3F2FD"][i],
                    fontSize: 12,
                    fontWeight: 600,
                    color: ["#2E7D32", "#C62828", "#1565C0"][i],
                    textAlign: "center",
                  }}
                >
                  {["✍️", "🛡️", "🎨"][i]} {name}
                </div>
              ))}
            </div>

            <AgentLog logs={logs} isGenerating={isGenerating} />

            {!isGenerating && logs.length > 0 && (
              <button
                onClick={() => setTab("viewer")}
                style={{
                  marginTop: 16,
                  padding: "12px 24px",
                  borderRadius: 12,
                  border: "none",
                  background: "#7E57C2",
                  color: "white",
                  fontSize: 14,
                  fontWeight: 600,
                  cursor: "pointer",
                }}
              >
                📖 스토리북 보기
              </button>
            )}
          </div>
        )}

        {/* --- VIEWER TAB --- */}
        {tab === "viewer" && (
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
              <div>
                <h2 style={{ margin: 0, color: "#2D2D3F" }}>{story.title}</h2>
                <p style={{ margin: 0, marginTop: 4, color: "#888", fontSize: 14 }}>{story.genre} · 수채화풍</p>
              </div>
              <button
                onClick={() => {
                  setShowPrompt(null);
                }}
                style={{
                  padding: "8px 16px",
                  borderRadius: 8,
                  border: "1.5px solid #7E57C2",
                  background: "white",
                  color: "#7E57C2",
                  fontSize: 12,
                  fontWeight: 600,
                  cursor: "pointer",
                }}
              >
                🔗 공유하기
              </button>
            </div>

            <StorybookViewer story={story} />

            {/* Prompt viewer */}
            <div style={{ marginTop: 24, padding: 20, background: "#F9F9F9", borderRadius: 12 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: "#666", marginBottom: 12 }}>
                🔍 씬별 Gemini 이미지 프롬프트 (클릭하여 확인)
              </div>
              <div style={{ display: "flex", gap: 8 }}>
                {story.scenes.map((scene) => (
                  <button
                    key={scene.id}
                    onClick={() => setShowPrompt(showPrompt === scene.id ? null : scene.id)}
                    style={{
                      flex: 1,
                      padding: "8px 12px",
                      borderRadius: 8,
                      border: showPrompt === scene.id ? "1.5px solid #7E57C2" : "1.5px solid #DDD",
                      background: showPrompt === scene.id ? "#F3E5F5" : "white",
                      fontSize: 12,
                      cursor: "pointer",
                      fontWeight: showPrompt === scene.id ? 600 : 400,
                      color: showPrompt === scene.id ? "#7E57C2" : "#888",
                    }}
                  >
                    씬 {scene.id}
                  </button>
                ))}
              </div>
              {showPrompt && (
                <pre style={{
                  marginTop: 12,
                  padding: 16,
                  background: "#1a1a2e",
                  borderRadius: 8,
                  color: "#B0BEC5",
                  fontSize: 12,
                  lineHeight: 1.6,
                  whiteSpace: "pre-wrap",
                  overflow: "auto",
                }}>
                  {story.scenes.find((s) => s.id === showPrompt)?.imagePrompt}
                </pre>
              )}
            </div>
          </div>
        )}

        {/* --- GALLERY TAB --- */}
        {tab === "gallery" && (
          <div>
            <h2 style={{ margin: 0, marginBottom: 8, color: "#2D2D3F" }}>갤러리</h2>
            <p style={{ color: "#888", marginTop: 0, marginBottom: 24, fontSize: 14 }}>
              생성된 작품을 저장하고 공유할 수 있습니다.
            </p>

            <div style={{
              display: "grid",
              gridTemplateColumns: "repeat(2, 1fr)",
              gap: 20,
            }}>
              {story.scenes.map((scene) => (
                <div
                  key={scene.id}
                  style={{
                    borderRadius: 16,
                    overflow: "hidden",
                    background: scene.bgColor,
                    boxShadow: "0 2px 12px rgba(0,0,0,0.06)",
                    cursor: "pointer",
                    transition: "transform 0.2s",
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.transform = "translateY(-2px)")}
                  onMouseLeave={(e) => (e.currentTarget.style.transform = "translateY(0)")}
                >
                  <SceneImage scene={scene} />
                  <div style={{ padding: "12px 16px" }}>
                    <div style={{ fontWeight: 700, fontSize: 14, color: "#333" }}>
                      {scene.id}. {scene.title}
                    </div>
                    <div style={{
                      fontSize: 12,
                      color: "#888",
                      marginTop: 4,
                      display: "-webkit-box",
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: "vertical",
                      overflow: "hidden",
                    }}>
                      {scene.narration.split("\n")[0]}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div style={{
              marginTop: 24,
              padding: 16,
              background: "#F5F5F5",
              borderRadius: 12,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}>
              <div>
                <div style={{ fontWeight: 600, fontSize: 14, color: "#333" }}>{story.title}</div>
                <div style={{ fontSize: 12, color: "#888", marginTop: 2 }}>
                  /works/abc123 · {story.scenes.length}컷 · {story.genre}
                </div>
              </div>
              <div style={{ display: "flex", gap: 8 }}>
                <button style={{
                  padding: "8px 16px", borderRadius: 8, border: "1.5px solid #4CAF50",
                  background: "white", color: "#4CAF50", fontSize: 12, fontWeight: 600, cursor: "pointer",
                }}>
                  💾 저장
                </button>
                <button style={{
                  padding: "8px 16px", borderRadius: 8, border: "none",
                  background: "#5C6BC0", color: "white", fontSize: 12, fontWeight: 600, cursor: "pointer",
                }}>
                  🔗 공유
                </button>
              </div>
            </div>
          </div>
        )}

        {/* --- REPORT TAB --- */}
        {tab === "report" && (
          <div>
            <h2 style={{ margin: 0, marginBottom: 8, color: "#2D2D3F" }}>캐릭터 일관성 검증</h2>
            <p style={{ color: "#888", marginTop: 0, marginBottom: 24, fontSize: 14 }}>
              work_id: abc123 · 주인공 '달'의 외형 특징이 각 씬에서 유지되는지 검증합니다.
            </p>
            <ConsistencyReport story={story} />
          </div>
        )}
      </main>
    </div>
  );
}
