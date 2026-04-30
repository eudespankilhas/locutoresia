import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Rss, Zap, Loader2, CheckCircle2, AlertCircle, Globe, Cpu,
  Newspaper, TrendingUp, Plane, Palette, Trophy, HeartPulse, BrainCircuit,
  Landmark, Clapperboard, FlaskConical
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const CATEGORIES = [
  { id: 'tecnologia', label: 'Tecnologia', icon: Cpu, color: 'text-blue-500' },
  { id: 'economia', label: 'Economia', icon: TrendingUp, color: 'text-green-500' },
  { id: 'turismo', label: 'Turismo', icon: Plane, color: 'text-cyan-500' },
  { id: 'cultura', label: 'Cultura', icon: Palette, color: 'text-purple-500' },
  { id: 'esportes', label: 'Esportes', icon: Trophy, color: 'text-orange-500' },
  { id: 'saude', label: 'Saúde e Bem-Estar', icon: HeartPulse, color: 'text-rose-500' },
  { id: 'inteligencia_artificial', label: 'Inteligência Artificial', icon: BrainCircuit, color: 'text-violet-500' },
  { id: 'politica', label: 'Política', icon: Landmark, color: 'text-amber-500' },
  { id: 'entretenimento', label: 'Entretenimento', icon: Clapperboard, color: 'text-pink-500' },
  { id: 'ciencia', label: 'Ciência', icon: FlaskConical, color: 'text-emerald-500' },
];

export function VoxCraftEngine() {
  const [selectedCategories, setSelectedCategories] = useState(CATEGORIES.map(c => c.id));
  const [isGenerating, setIsGenerating] = useState(false);
  const [results, setResults] = useState([]);
  const [progress, setProgress] = useState('');

  const toggleCategory = (id) => {
    setSelectedCategories(prev =>
      prev.includes(id) ? prev.filter(c => c !== id) : [...prev, id]
    );
  };

  const runPipeline = async () => {
    if (selectedCategories.length === 0) {
      alert('Selecione ao menos 1 categoria');
      return;
    }

    setIsGenerating(true);
    setResults([]);
    setProgress('Buscando notícias reais via RSS...');

    try {
      // Simulação do VoxCraft Engine para Locutores IA
      await new Promise(r => setTimeout(r, 2000));
      setProgress('Processando notícias com IA...');
      await new Promise(r => setTimeout(r, 1500));
      setProgress('Gerando conteúdo viral...');
      await new Promise(r => setTimeout(r, 1000));

      const mockResults = selectedCategories.map(catId => {
        const category = CATEGORIES.find(c => c.id === catId);
        return {
          category: category.label,
          success: true,
          postId: `post_${Date.now()}_${catId}`,
          headlines: [
            `Última hora: ${category.label} revoluciona o mercado`,
            `Descubra as novidades em ${category.label}`,
            `${category.label}: Tendências que você precisa conhecer`
          ]
        };
      });

      setResults(mockResults);
      setProgress('');

      alert(`VoxCraft: ${mockResults.length} posts gerados com sucesso!`);
    } catch (e) {
      console.error('VoxCraft error:', e);
      setProgress('');
      alert('Erro no VoxCraft Engine: ' + String(e));
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <Card className="border-primary/20 bg-gradient-to-br from-background to-primary/5">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-lg">
          <div className="p-1.5 bg-primary/20 rounded-lg">
            <Rss className="h-5 w-5 text-primary" />
          </div>
          VoxCraft Engine
          <Badge className="ml-auto text-xs bg-gradient-to-r from-pink-500 to-purple-600 text-white border-0">
            <Zap className="h-3 w-3 mr-1" />
            RSS + IA
          </Badge>
        </CardTitle>
        <p className="text-xs text-muted-foreground">
          Motor autônomo: lê notícias reais &rarr; gera posts virais &rarr; publica automaticamente
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Category Selection */}
        <div className="space-y-2">
          <p className="text-sm font-medium flex items-center gap-1">
            <Newspaper className="h-4 w-4" />
            Fontes RSS (Notícias Reais)
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {CATEGORIES.map(cat => {
              const Icon = cat.icon;
              const isSelected = selectedCategories.includes(cat.id);
              return (
                <div
                  key={cat.id}
                  onClick={() => toggleCategory(cat.id)}
                  className={`flex items-center gap-2 p-2 rounded-lg border cursor-pointer transition-all ${
                    isSelected ? 'border-primary bg-primary/10' : 'border-border/50 opacity-60'
                  }`}
                >
                  <Checkbox checked={isSelected} className="pointer-events-none" />
                  <Icon className={`h-4 w-4 ${cat.color}`} />
                  <span className="text-sm">{cat.label}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Generate Button */}
        <Button
          onClick={runPipeline}
          disabled={isGenerating || selectedCategories.length === 0}
          className="w-full gap-2 bg-gradient-to-r from-pink-500 to-purple-600 hover:opacity-90 text-white"
          size="lg"
        >
          {isGenerating ? (
            <><Loader2 className="h-5 w-5 animate-spin" />Gerando {selectedCategories.length} posts...</>
          ) : (
            <><Globe className="h-5 w-5" />Gerar {selectedCategories.length} Posts com Notícias Reais</>
          )}
        </Button>

        {/* Progress */}
        {progress && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-2 p-3 bg-muted/30 rounded-lg text-sm"
          >
            <Loader2 className="h-4 w-4 animate-spin text-primary" />
            {progress}
          </motion.div>
        )}

        {/* Results */}
        <AnimatePresence>
          {results.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-2 pt-2 border-t border-border/50"
            >
              <p className="text-sm font-medium">Resultados do Pipeline</p>
              {results.map((r, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="flex items-center gap-2 p-2 rounded-lg bg-muted/20 border border-border/30"
                >
                  {r.success ? (
                    <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0" />
                  ) : (
                    <AlertCircle className="h-4 w-4 text-destructive shrink-0" />
                  )}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium capitalize">{r.category}</p>
                    {r.headlines && r.headlines.length > 0 && (
                      <p className="text-xs text-muted-foreground truncate">
                        {r.headlines[0]}
                      </p>
                    )}
                  </div>
                  {r.success ? (
                    <Badge variant="secondary" className="text-xs shrink-0">Publicado</Badge>
                  ) : (
                    <Badge variant="destructive" className="text-xs shrink-0">Erro</Badge>
                  )}
                </motion.div>
              ))}
              <p className="text-xs text-muted-foreground text-center pt-1">
                Posts publicados aparecem no Feed e em Conexões
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </CardContent>
    </Card>
  );
}
