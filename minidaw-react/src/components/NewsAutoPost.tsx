import React, { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Newspaper, Play, Pause, RefreshCw, Clock, Check,
  AlertCircle, Loader2, Globe, Zap, Eye
} from "lucide-react";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

const NEWS_SOURCES = [
  { id: "exame", label: "Exame", url: "https://exame.com", emoji: "https://exame.com" },
  { id: "folha", label: "Folha de S.Paulo", url: "https://folha.uol.com.br", emoji: "https://folha.uol.com.br" },
  { id: "diario_nordeste", label: "Diário do Nordeste", url: "https://diariodonordeste.verdesmares.com.br", emoji: "https://diariodonordeste.verdesmares.com.br" },
  { id: "veja", label: "Veja", url: "https://veja.abril.com.br", emoji: "https://veja.abril.com.br" },
];

const INTERVAL_MS = 60 * 60 * 1000; // 1 hora

export default function NewsAutoPost() {
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState([]);
  const [nextRunIn, setNextRunIn] = useState(null);
  const [lastRun, setLastRun] = useState(null);
  const [isPosting, setIsPosting] = useState(false);
  const [enabledSources, setEnabledSources] = useState(
    Object.fromEntries(NEWS_SOURCES.map(s => [s.id, true]))
  );
  const [previewNews, setPreviewNews] = useState(null);

  const intervalRef = useRef(null);
  const countdownRef = useRef(null);
  const logsEndRef = useRef(null);

  useEffect(() => {
    return () => {
      clearInterval(intervalRef.current);
      clearInterval(countdownRef.current);
    };
  }, []);

  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs]);

  const addLog = (message, type = "info") => {
    setLogs(prev => [...prev, { message, type, time: new Date() }]);
  };

  const fetchAndPostNews = async () => {
    const activeSources = NEWS_SOURCES.filter(s => enabledSources[s.id]);
    if (activeSources.length === 0) {
      addLog("Nenhuma fonte ativa. Ative ao menos uma fonte.", "warn");
      return;
    }

    setIsPosting(true);
    const source = activeSources[Math.floor(Math.random() * activeSources.length)];
    addLog(`Buscando notícias em: ${source.label}...`, "info");

    try {
      // Chamar API backend
      const response = await fetch('http://localhost:5000/api/news/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ enabled_sources: enabledSources })
      });

      const result = await response.json();

      if (result.success) {
        setPreviewNews(result);
        addLog(`Notícia encontrada: "${result.title}"`, "success");

        // Publicar na NewPost-IA
        addLog("Publicando na NewPost-IA...", "info");
        await publishToNewPostIA({
          content: `${result.title}\n\n${result.summary}\n\nFonte: ${result.source}`,
          hashtags: [],
        });
        addLog(`Publicado com sucesso!`, "success");
      } else {
        addLog(`Erro ao buscar notícia: ${result.error || "sem dados"}`, "error");
      }
    } catch (error) {
      addLog(`Erro: ${error.message}`, "error");
    }

    setLastRun(new Date());
    setIsPosting(false);
  };

  const startAutomation = async () => {
    if (isRunning) return;
    
    try {
      const response = await fetch('http://localhost:5000/api/news/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ enabled_sources: enabledSources })
      });

      if (response.ok) {
        setIsRunning(true);
        addLog("Automação iniciada!", "success");
        startCountdown();
      } else {
        addLog("Erro ao iniciar automação", "error");
      }
    } catch (error) {
      addLog(`Erro: ${error.message}`, "error");
    }
  };

  const stopAutomation = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/news/stop', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        setIsRunning(false);
        setNextRunIn(null);
        clearInterval(countdownRef.current);
        addLog("Automação pausada.", "warn");
      }
    } catch (error) {
      addLog(`Erro: ${error.message}`, "error");
    }
  };

  const startCountdown = () => {
    let secondsLeft = 10; // 10 segundos para teste
    setNextRunIn(secondsLeft);
    countdownRef.current = setInterval(() => {
      secondsLeft -= 1;
      if (secondsLeft <= 0) {
        secondsLeft = 10; // Reset
        fetchStatus(); // Atualizar status
      }
      setNextRunIn(secondsLeft);
    }, 1000);
  };

  const fetchStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/news/status');
      const status = await response.json();
      
      setLogs(status.logs.map(log => ({
        ...log,
        time: new Date(log.time)
      })));
      setLastRun(status.last_run ? new Date(status.last_run) : null);
      setPreviewNews(status.news_published > 0 ? { title: "Última notícia publicada" } : null);
    } catch (error) {
      console.error('Erro ao buscar status:', error);
    }
  };

  useEffect(() => {
    if (isRunning) {
      const interval = setInterval(fetchStatus, 5000); // Atualizar a cada 5 segundos
      return () => clearInterval(interval);
    }
  }, [isRunning]);

  const formatCountdown = (s) => {
    if (!s) return "--";
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return `${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
  };

  const LOG_COLORS = {
    info: "text-slate-400",
    success: "text-green-400",
    error: "text-red-400",
    warn: "text-yellow-400",
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-900 p-6">
      <div className="max-w-4xl mx-auto space-y-6">

        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-white via-purple-200 to-blue-200 bg-clip-text text-transparent mb-1">
            News Auto Post
          </h1>
          <p className="text-slate-400">Busca notícias reais a cada 10 segundos e publica automaticamente</p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Control panel */}
          <div className="space-y-4">
            {/* Status card */}
            <Card className="bg-slate-900/60 border-purple-800/30 shadow-xl">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2 text-base">
                  <Zap className="w-4 h-4 text-yellow-400" />
                  Status da Automação
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className={`w-2.5 h-2.5 rounded-full ${isRunning ? "bg-green-400 animate-pulse" : "bg-slate-600"}`} />
                    <span className={`text-sm font-medium ${isRunning ? "text-green-400" : "text-slate-400"}`}>
                      {isRunning ? "Rodando" : "Pausado"}
                    </span>
                  </div>
                  {isRunning && nextRunIn && (
                    <div className="flex items-center gap-1.5 bg-slate-800/60 border border-slate-700 rounded-lg px-3 py-1">
                      <Clock className="w-3.5 h-3.5 text-blue-400" />
                      <span className="text-blue-300 text-sm font-mono">{formatCountdown(nextRunIn)}</span>
                      <span className="text-slate-500 text-xs">próximo</span>
                    </div>
                  )}
                </div>

                {lastRun && (
                  <p className="text-xs text-slate-500">
                    Última execução: {format(lastRun, "dd/MM HH:mm:ss", { locale: ptBR })}
                  </p>
                )}

                <div className="flex gap-2">
                  {!isRunning ? (
                    <Button
                      onClick={startAutomation}
                      className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700"
                    >
                      <Play className="w-4 h-4 mr-2" /> Iniciar Automação
                    </Button>
                  ) : (
                    <Button
                      onClick={stopAutomation}
                      variant="outline"
                      className="flex-1 border-red-700/50 text-red-400 hover:bg-red-900/20"
                    >
                      <Pause className="w-4 h-4 mr-2" /> Pausar
                    </Button>
                  )}
                  <Button
                    onClick={fetchAndPostNews}
                    disabled={isPosting}
                    variant="outline"
                    className="border-blue-700/50 text-blue-400 hover:bg-blue-900/20"
                    title="Executar agora"
                  >
                    {isPosting ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Sources */}
            <Card className="bg-slate-900/60 border-purple-800/30 shadow-xl">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2 text-base">
                  <Globe className="w-4 h-4 text-cyan-400" />
                  Fontes de Notícias
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {NEWS_SOURCES.map(source => (
                  <div key={source.id} className="flex items-center justify-between p-2.5 bg-slate-800/40 rounded-xl border border-slate-700/50">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{source.emoji}</span>
                      <div>
                        <p className="text-white text-sm font-medium">{source.label}</p>
                        <p className="text-slate-500 text-xs">{source.url}</p>
                      </div>
                    </div>
                    <Switch
                      checked={enabledSources[source.id]}
                      onCheckedChange={(v) => setEnabledSources(prev => ({ ...prev, [source.id]: v }))}
                    />
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Right side */}
          <div className="space-y-4">
            {/* Preview */}
            {previewNews && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                <Card className="bg-green-900/20 border-green-700/40 shadow-xl">
                  <CardHeader>
                    <CardTitle className="text-green-300 text-sm flex items-center gap-2">
                      <Eye className="w-4 h-4" /> Última notícia postada
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex items-start gap-2">
                      <span className="text-xl">:)</span>
                      <div>
                        <p className="text-white text-sm font-semibold">{previewNews.title}</p>
                        <p className="text-slate-400 text-xs mt-1">{previewNews.summary || "Notícia publicada com sucesso"}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge className="bg-green-500/20 text-green-300 text-xs">
                        Publicado
                      </Badge>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {/* Log console */}
            <Card className="bg-slate-900/60 border-purple-800/30 shadow-xl">
              <CardHeader>
                <CardTitle className="text-white text-sm flex items-center gap-2">
                  <Newspaper className="w-4 h-4 text-purple-400" />
                  Log de Execuções
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-3 h-64 overflow-y-auto font-mono text-xs space-y-1">
                  {logs.length === 0 ? (
                    <p className="text-slate-600 text-center py-8">Nenhuma execução ainda. Clique em "Iniciar Automação".</p>
                  ) : (
                    logs.map((log, i) => (
                      <div key={i} className={`flex gap-2 ${LOG_COLORS[log.type]}`}>
                        <span className="text-slate-700 shrink-0">{format(log.time, "HH:mm:ss")}</span>
                        <span>{log.message}</span>
                      </div>
                    ))
                  )}
                  <div ref={logsEndRef} />
                </div>
                {logs.length > 0 && (
                  <button onClick={() => setLogs([])} className="text-xs text-slate-600 hover:text-slate-400 mt-2 transition-colors">
                    Limpar log
                  </button>
                )}
              </CardContent>
            </Card>

            {/* Info box */}
            <div className="p-3 bg-green-900/20 border border-green-700/30 rounded-xl text-xs space-y-2">
              <p className="text-green-300 font-medium flex items-center gap-1.5">
                <Zap className="w-3 h-3" /> Automação Backend Ativa
              </p>
              <p className="text-slate-400">Uma automação backend roda a cada 10 segundos (teste), buscando notícias reais e publicando continuamente.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
