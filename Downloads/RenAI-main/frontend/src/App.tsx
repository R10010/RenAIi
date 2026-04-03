import React, { useState, useEffect } from 'react';
import Avatar3D from './components/Avatar3D';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [avatarState, setAvatarState] = useState<any>(null);

  const sendMessage = async () => {
    const res = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: input, user_id: 'test' })
    });
    const data = await res.json();
    setAvatarState(data.avatar);
    setInput('');
  };

  return (
    <div className="app">
      <h1>RenAI 3D Avatar</h1>
      <div className="avatar-container">
        {avatarState && (
          <Avatar3D 
            blendshapeWeights={avatarState.blendshape_weights} 
            emotion={avatarState.emotion} 
          />
        )}
      </div>
      <div className="chat-input">
        <input 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type something..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
      {avatarState && <div>Emotion: {avatarState.emotion}</div>}
    </div>
  );
}

export default App;