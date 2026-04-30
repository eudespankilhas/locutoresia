import React, { useState, useEffect } from "react";

const NEWS_SOURCES = [
  { id: "exame", label: "Exame", url: "https://exame.com" },
  { id: "folha", label: "Folha de S.Paulo", url: "https://folha.uol.com.br" },
  { id: "diario_nordeste", label: "Diário do Nordeste", url: "https://diariodonordeste.verdesmares.com.br" },
  { id: "veja", label: "Veja", url: "https://veja.abril.com.br" },
];

export default function NewsAutoPostUltraSimple() {
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState([]);
  const [isPosting, setIsPosting] = useState(false);
  const [enabledSources, setEnabledSources] = useState(
    Object.fromEntries(NEWS_SOURCES.map(s => [s.id, true]))
  );
  const [previewNews, setPreviewNews] = useState(null);

  useEffect(() => {
    fetchStatus();
  }, []);

  const addLog = (message, type = "info") => {
    setLogs(prev => [...prev, { message, type, time: new Date() }]);
  };

  const fetchStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/news/status');
      const status = await response.json();
      setIsRunning(status.is_running);
      setLogs(status.logs.map(log => ({
        ...log,
        time: new Date(log.time)
      })));
    } catch (error) {
      console.error('Erro ao buscar status:', error);
    }
  };

  const fetchAndPostNews = async () => {
    setIsPosting(true);
    addLog("Buscando notícia...", "info");

    try {
      const response = await fetch('http://localhost:5000/api/news/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled_sources: enabledSources })
      });

      const result = await response.json();

      if (result.success) {
        setPreviewNews(result);
        addLog(`Notícia encontrada: ${result.title}`, "success");

        // Publicar
        await publishToNewPostIA({
          content: `${result.title}\n\n${result.summary}`,
          hashtags: []
        });
        addLog("Publicado com sucesso!", "success");
      } else {
        addLog("Erro ao buscar notícia", "error");
      }
    } catch (error) {
      addLog(`Erro: ${error.message}`, "error");
    }

    setIsPosting(false);
  };

  const publishToNewPostIA = async (data) => {
    try {
      const response = await fetch('http://localhost:5000/api/newpost/publish', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      return await response.json();
    } catch (error) {
      console.error('Erro ao publicar:', error);
      throw error;
    }
  };

  const startAutomation = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/news/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled_sources: enabledSources })
      });

      if (response.ok) {
        setIsRunning(true);
        addLog("Automação iniciada!", "success");
      }
    } catch (error) {
      addLog(`Erro: ${error.message}`, "error");
    }
  };

  const stopAutomation = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/news/stop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      if (response.ok) {
        setIsRunning(false);
        addLog("Automação parada", "warn");
      }
    } catch (error) {
      addLog(`Erro: ${error.message}`, "error");
    }
  };

  const toggleSource = (sourceId) => {
    setEnabledSources(prev => ({
      ...prev,
      [sourceId]: !prev[sourceId]
    }));
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  const getLogColor = (type) => {
    switch(type) {
      case 'success': return 'text-green-400';
      case 'error': return 'text-red-400';
      case 'warn': return 'text-yellow-400';
      default: return 'text-slate-400';
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(to bottom right, #0f172a, #581c87, #0f172a)', padding: '24px' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', color: 'white' }}>
        
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h1 style={{ fontSize: '48px', fontWeight: 'bold', background: 'linear-gradient(to right, white, #e0e7ff, #c7d2fe)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', marginBottom: '8px' }}>
            News Auto Post
          </h1>
          <p style={{ color: '#94a3b8' }}>Sistema ultra simplificado de notícias automáticas</p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          
          {/* Painel de Controle */}
          <div>
            <div style={{ background: '#1e293b', border: '1px solid #6b21a8', borderRadius: '12px', padding: '20px', marginBottom: '24px' }}>
              <h2 style={{ color: 'white', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ color: '#facc15' }}>Status</span>
              </h2>
              
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: isRunning ? '#4ade80' : '#64748b' }} />
                  <span style={{ fontSize: '14px', color: isRunning ? '#4ade80' : '#94a3b8' }}>
                    {isRunning ? 'Rodando' : 'Pausado'}
                  </span>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '8px' }}>
                {!isRunning ? (
                  <button
                    onClick={startAutomation}
                    style={{ flex: 1, background: 'linear-gradient(to right, #16a34a, #059669)', color: 'white', border: 'none', padding: '12px', borderRadius: '8px', cursor: 'pointer' }}
                  >
                    Iniciar Automação
                  </button>
                ) : (
                  <button
                    onClick={stopAutomation}
                    style={{ flex: 1, background: 'transparent', color: '#ef4444', border: '1px solid #991b1b', padding: '12px', borderRadius: '8px', cursor: 'pointer' }}
                  >
                    Pausar
                  </button>
                )}
                <button
                  onClick={fetchAndPostNews}
                  disabled={isPosting}
                  style={{ background: 'transparent', color: '#3b82f6', border: '1px solid #1e40af', padding: '12px', borderRadius: '8px', cursor: 'pointer' }}
                >
                  {isPosting ? '...' : 'Executar'}
                </button>
              </div>
            </div>

            {/* Fontes */}
            <div style={{ background: '#1e293b', border: '1px solid #6b21a8', borderRadius: '12px', padding: '20px' }}>
              <h2 style={{ color: 'white', marginBottom: '16px' }}>Fontes de Notícias</h2>
              
              {NEWS_SOURCES.map(source => (
                <div key={source.id} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px', background: '#334155', borderRadius: '8px', marginBottom: '8px' }}>
                  <div>
                    <div style={{ color: 'white', fontSize: '14px', fontWeight: '500' }}>{source.label}</div>
                    <div style={{ color: '#64748b', fontSize: '12px' }}>{source.url}</div>
                  </div>
                  <button
                    onClick={() => toggleSource(source.id)}
                    style={{ width: '48px', height: '24px', borderRadius: '12px', backgroundColor: enabledSources[source.id] ? '#16a34a' : '#64748b', border: 'none', cursor: 'pointer', position: 'relative' }}
                  >
                    <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: 'white', position: 'absolute', top: '2px', left: enabledSources[source.id] ? '26px' : '2px', transition: 'all 0.2s' }} />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Logs */}
          <div>
            {previewNews && (
              <div style={{ background: '#14532d', border: '1px solid #16a34a', borderRadius: '12px', padding: '20px', marginBottom: '24px' }}>
                <h3 style={{ color: '#4ade80', marginBottom: '12px' }}>Última Notícia</h3>
                <div style={{ color: 'white', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>{previewNews.title}</div>
                <div style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '8px' }}>{previewNews.summary}</div>
                <div style={{ background: '#166534', color: '#4ade80', fontSize: '12px', padding: '4px 8px', borderRadius: '4px', display: 'inline-block' }}>
                  Publicado
                </div>
              </div>
            )}

            <div style={{ background: '#1e293b', border: '1px solid #6b21a8', borderRadius: '12px', padding: '20px' }}>
              <h2 style={{ color: 'white', marginBottom: '16px' }}>Logs</h2>
              
              <div style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', padding: '12px', height: '300px', overflowY: 'auto', fontFamily: 'monospace', fontSize: '12px' }}>
                {logs.length === 0 ? (
                  <div style={{ color: '#64748b', textAlign: 'center', padding: '32px' }}>
                    Nenhuma execução ainda
                  </div>
                ) : (
                  logs.map((log, i) => (
                    <div key={i} style={{ display: 'flex', gap: '8px', marginBottom: '4px', color: getLogColor(log.type) }}>
                      <span style={{ color: '#475569' }}>{formatTime(log.time)}</span>
                      <span>{log.message}</span>
                    </div>
                  ))
                )}
              </div>

              {logs.length > 0 && (
                <button
                  onClick={() => setLogs([])}
                  style={{ marginTop: '12px', background: 'transparent', color: '#64748b', border: 'none', fontSize: '12px', cursor: 'pointer' }}
                >
                  Limpar log
                </button>
              )}
            </div>
          </div>
        </div>

        <div style={{ marginTop: '24px', background: '#14532d', border: '1px solid #16a34a', borderRadius: '12px', padding: '16px' }}>
          <div style={{ color: '#4ade80', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>Sistema Funcionando</div>
          <div style={{ color: '#94a3b8', fontSize: '12px' }}>
            Backend: http://localhost:5000 | Frontend: http://localhost:3002
          </div>
        </div>

      </div>
    </div>
  );
}
