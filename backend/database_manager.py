# Gerenciador do Banco de Dados - Supabase
from supabase_config import get_supabase_client, CREATE_TABLES_SQL
from datetime import datetime, date
from typing import List, Dict, Optional
import json

class DatabaseManager:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def setup_database(self):
        """Cria tabelas no banco de dados"""
        try:
            # Executar SQL para criar tabelas
            result = self.supabase.rpc('exec_sql', {'sql': CREATE_TABLES_SQL}).execute()
            print("Banco de dados configurado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao configurar banco: {e}")
            return False
    
    def save_publication(self, publication_data: Dict) -> bool:
        """Salva uma publicação no banco"""
        try:
            result = self.supabase.table('publications').insert({
                'content': publication_data.get('content'),
                'hashtags': publication_data.get('hashtags', []),
                'source': publication_data.get('source'),
                'published_to': publication_data.get('published_to'),
                'status': publication_data.get('status', 'published'),
                'newpost_id': publication_data.get('newpost_id'),
                'title': publication_data.get('title'),
                'summary': publication_data.get('summary'),
                'link': publication_data.get('link')
            }).execute()
            
            # Salvar log
            self.save_log(f"Publicação salva: {publication_data.get('title', 'Sem título')}", 'success')
            return True
        except Exception as e:
            self.save_log(f"Erro ao salvar publicação: {str(e)}", 'error')
            return False
    
    def save_log(self, message: str, log_type: str = 'info', publication_id: Optional[int] = None) -> bool:
        """Salva um log no banco"""
        try:
            self.supabase.table('logs').insert({
                'message': message,
                'type': log_type,
                'publication_id': publication_id
            }).execute()
            return True
        except Exception as e:
            print(f"Erro ao salvar log: {e}")
            return False
    
    def get_publications(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Busca publicações com paginação"""
        try:
            result = self.supabase.table('publications')\
                .select('*')\
                .order('published_at', desc=True)\
                .range(offset, offset + limit - 1)\
                .execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Erro ao buscar publicações: {e}")
            return []
    
    def get_logs(self, limit: int = 100, log_type: Optional[str] = None) -> List[Dict]:
        """Busca logs do sistema"""
        try:
            query = self.supabase.table('logs').select('*').order('created_at', desc=True)
            if log_type:
                query = query.eq('type', log_type)
            
            result = query.limit(limit).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Erro ao buscar logs: {e}")
            return []
    
    def get_sources(self) -> List[Dict]:
        """Busca fontes de notícias configuradas"""
        try:
            result = self.supabase.table('sources').select('*').execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Erro ao buscar fontes: {e}")
            return []
    
    def update_source_last_fetch(self, source_id: str) -> bool:
        """Atualiza último fetch de uma fonte"""
        try:
            self.supabase.table('sources')\
                .update({'last_fetch': datetime.now().isoformat()})\
                .eq('id', source_id)\
                .execute()
            return True
        except Exception as e:
            print(f"Erro ao atualizar fonte: {e}")
            return False
    
    def get_analytics(self, days: int = 7) -> List[Dict]:
        """Busca analytics dos últimos dias"""
        try:
            result = self.supabase.table('analytics')\
                .select('*')\
                .gte('date', date.fromordinal(date.today().toordinal() - days))\
                .order('date', desc=True)\
                .execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Erro ao buscar analytics: {e}")
            return []
    
    def update_daily_analytics(self) -> bool:
        """Atualiza analytics diários"""
        try:
            today = date.today().isoformat()
            
            # Buscar publicações de hoje
            result = self.supabase.table('publications')\
                .select('*')\
                .eq('published_at::date', today)\
                .execute()
            
            publications = result.data if result.data else []
            
            # Contar estatísticas
            total_count = len(publications)
            success_count = len([p for p in publications if p.get('status') == 'published'])
            error_count = total_count - success_count
            
            # Fonte mais usada
            sources_count = {}
            for pub in publications:
                source = pub.get('source', 'unknown')
                sources_count[source] = sources_count.get(source, 0) + 1
            
            most_used = max(sources_count.items(), key=lambda x: x[1])[0] if sources_count else None
            
            # Inserir ou atualizar analytics
            analytics_data = {
                'date': today,
                'publications_count': total_count,
                'success_count': success_count,
                'error_count': error_count,
                'most_used_source': most_used
            }
            
            # Tentar atualizar primeiro
            existing = self.supabase.table('analytics')\
                .select('*')\
                .eq('date', today)\
                .execute()
            
            if existing.data:
                self.supabase.table('analytics')\
                    .update(analytics_data)\
                    .eq('date', today)\
                    .execute()
            else:
                self.supabase.table('analytics').insert(analytics_data).execute()
            
            return True
        except Exception as e:
            print(f"Erro ao atualizar analytics: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas gerais do sistema"""
        try:
            # Total de publicações
            pub_result = self.supabase.table('publications').select('id', count='exact').execute()
            total_publications = pub_result.count if pub_result.count else 0
            
            # Logs recentes
            logs_result = self.supabase.table('logs')\
                .select('*')\
                .order('created_at', desc=True)\
                .limit(10)\
                .execute()
            
            # Fontes ativas
            sources_result = self.supabase.table('sources')\
                .select('*')\
                .eq('enabled', True)\
                .execute()
            
            return {
                'total_publications': total_publications,
                'recent_logs': logs_result.data if logs_result.data else [],
                'active_sources': len(sources_result.data if sources_result.data else []),
                'sources': sources_result.data if sources_result.data else []
            }
        except Exception as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return {
                'total_publications': 0,
                'recent_logs': [],
                'active_sources': 0,
                'sources': []
            }

# Instância global do gerenciador
db_manager = DatabaseManager()
