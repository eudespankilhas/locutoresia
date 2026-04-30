import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Brain, 
  Calendar, 
  TrendingUp, 
  RefreshCw, 
  Sparkles,
  Users,
  Zap,
  BarChart3,
  Clock,
  CalendarClock,
  History as HistoryIcon
} from 'lucide-react';
import { motion } from 'framer-motion';
import { AIContentPlanner } from './AIContentPlanner.jsx';

interface AutonomousAIDashboardProps {
  onApplyContent?: (content: string) => void;
}

export function AutonomousAIDashboard({ onApplyContent }: AutonomousAIDashboardProps) {
  const [activeTab, setActiveTab] = useState('planner');

  const features = [
    {
      icon: Calendar,
      title: 'Calendário Autônomo',
      description: 'Pipeline de Multi-Agentes cria calendário completo',
      color: 'text-blue-500',
      bg: 'bg-blue-500/10',
    },
    {
      icon: TrendingUp,
      title: 'Análise Preditiva',
      description: 'Preveja engajamento ANTES de publicar',
      color: 'text-green-500',
      bg: 'bg-green-500/10',
    },
    {
      icon: RefreshCw,
      title: 'Otimização Contínua',
      description: 'Sugestões em tempo real para melhorar posts',
      color: 'text-purple-500',
      bg: 'bg-purple-500/10',
    },
    {
      icon: Users,
      title: 'Multi-Agentes',
      description: 'Pesquisador &rarr; Estrategista &rarr; Escritor &rarr; Revisor',
      color: 'text-orange-500',
      bg: 'bg-orange-500/10',
    },
  ];

  return (
    <Card className="border-primary/20 bg-gradient-to-br from-background via-primary/5 to-background">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-xl">
          <div className="p-2 bg-primary/20 rounded-lg">
            <Brain className="h-6 w-6 text-primary" />
          </div>
          Central IA Autônoma
          <Badge className="ml-auto bg-gradient-hero text-white">
            <Zap className="h-3 w-3 mr-1" />
            Multi-Agentes
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Feature Overview */}
        <div className="grid grid-cols-2 gap-3">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`p-3 rounded-lg ${feature.bg} border border-border/50`}
            >
              <feature.icon className={`h-5 w-5 ${feature.color} mb-2`} />
              <p className="text-sm font-medium">{feature.title}</p>
              <p className="text-xs text-muted-foreground">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        {/* Main Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="w-full flex overflow-x-auto gap-1 p-1">
            <TabsTrigger value="planner" className="flex-1 min-w-0 gap-1 text-xs px-2 py-1.5">
              <Calendar className="h-3 w-3 shrink-0" />
              <span className="truncate">Calendário</span>
            </TabsTrigger>
            <TabsTrigger value="predict" className="flex-1 min-w-0 gap-1 text-xs px-2 py-1.5">
              <TrendingUp className="h-3 w-3 shrink-0" />
              <span className="truncate">Prever</span>
            </TabsTrigger>
            <TabsTrigger value="optimize" className="flex-1 min-w-0 gap-1 text-xs px-2 py-1.5">
              <RefreshCw className="h-3 w-3 shrink-0" />
              <span className="truncate">Otimizar</span>
            </TabsTrigger>
            <TabsTrigger value="schedule" className="flex-1 min-w-0 gap-1 text-xs px-2 py-1.5">
              <CalendarClock className="h-3 w-3 shrink-0" />
              <span className="truncate">Agendar</span>
            </TabsTrigger>
            <TabsTrigger value="history" className="flex-1 min-w-0 gap-1 text-xs px-2 py-1.5">
              <HistoryIcon className="h-3 w-3 shrink-0" />
              <span className="truncate">Histórico</span>
            </TabsTrigger>
            <TabsTrigger value="voxcraft" className="flex-1 min-w-0 gap-1 text-xs px-2 py-1.5">
              <Zap className="h-3 w-3 shrink-0" />
              <span className="truncate">VoxCraft</span>
            </TabsTrigger>
            <TabsTrigger value="curadoria" className="flex-1 min-w-0 gap-1 text-xs px-2 py-1.5">
              <BarChart3 className="h-3 w-3 shrink-0" />
              <span className="truncate">Curadoria</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="planner" className="mt-4">
            <AIContentPlanner />
          </TabsContent>

          <TabsContent value="predict" className="mt-4">
            <Card className="border-border/50">
              <CardContent className="p-4 text-center">
                <TrendingUp className="h-12 w-12 mx-auto mb-3 text-primary opacity-50" />
                <p className="text-sm text-muted-foreground">Análise Preditiva em desenvolvimento...</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="optimize" className="mt-4">
            <Card className="border-border/50">
              <CardContent className="p-4 text-center">
                <RefreshCw className="h-12 w-12 mx-auto mb-3 text-primary opacity-50" />
                <p className="text-sm text-muted-foreground">Otimização Contínua em desenvolvimento...</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="schedule" className="mt-4">
            <Card className="border-border/50">
              <CardContent className="p-4 text-center">
                <CalendarClock className="h-12 w-12 mx-auto mb-3 text-primary opacity-50" />
                <p className="text-sm text-muted-foreground">Agendamento Inteligente em desenvolvimento...</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="history" className="mt-4">
            <Card className="border-border/50">
              <CardContent className="p-4 text-center">
                <HistoryIcon className="h-12 w-12 mx-auto mb-3 text-primary opacity-50" />
                <p className="text-sm text-muted-foreground">Histórico de Predições em desenvolvimento...</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="voxcraft" className="mt-4">
            <Card className="border-border/50">
              <CardContent className="p-4 text-center">
                <Zap className="h-12 w-12 mx-auto mb-3 text-primary opacity-50" />
                <p className="text-sm text-muted-foreground">VoxCraft Engine em desenvolvimento...</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="curadoria" className="mt-4">
            <Card className="border-border/50">
              <CardContent className="p-4 text-center">
                <BarChart3 className="h-12 w-12 mx-auto mb-3 text-primary opacity-50" />
                <p className="text-sm text-muted-foreground">Sistema de Curadoria em desenvolvimento...</p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Stats Footer */}
        <div className="flex items-center justify-between pt-3 border-t border-border/50">
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              Atualizado em tempo real
            </span>
            <span className="flex items-center gap-1">
              <BarChart3 className="h-3 w-3" />
              ML Score Ativo
            </span>
          </div>
          <Badge variant="outline" className="text-xs">
            <Sparkles className="h-3 w-3 mr-1 text-primary" />
            Gemini 2.5 Flash
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}
