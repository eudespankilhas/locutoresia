"""
Teste simples da integração LMNT
"""

import sys
import os
sys.path.append('backend')

try:
    from lmnt_integration import lmnt_integration
    
    print("=== TESTE DE INTEGRAÇÃO LMNT ===")
    
    # Testar status
    status = lmnt_integration.get_status()
    print("Status:", status)
    
    if status.get('status') == 'available':
        print("✅ LMNT disponível")
        
        # Testar vozes
        voices = lmnt_integration.get_available_voices()
        print(f"✅ Vozes disponíveis: {len(voices.get('voices', []))}")
        
        # Testar geração
        result = lmnt_integration.generate_speech('Teste de integração!', 'amy')
        if 'success' in result:
            print(f"✅ Áudio gerado: {result['filename']}")
        else:
            print(f"❌ Erro: {result.get('error')}")
    else:
        print("❌ LMNT não disponível")
        print(f"Motivo: {status.get('message')}")
        
except Exception as e:
    print(f"❌ Erro no teste: {e}")
    import traceback
    traceback.print_exc()
