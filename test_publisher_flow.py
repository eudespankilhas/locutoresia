import sys
import os
from pprint import pprint

# Ensure the backend module is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from backend.social_post_publisher import social_publisher

def test_flow():
    print("=== TESTANDO FLUXO SOCIAL_POST_PUBLISHER ===")
    
    # 1. Criar um post de teste
    print("\n1. Criando post de rascunho...")
    create_res = social_publisher.create_post(
        title="Teste Automatizado: Publicação NewPost-IA",
        caption="Este é um teste automatizado para verificar a integração com a NewPost-IA.",
        hashtags=["teste", "automacao", "ia"],
        platforms=["newpost_ia"],
        status="rascunho"
    )
    
    if not create_res.get("success"):
        print("FALHA AO CRIAR POST:")
        pprint(create_res)
        return
        
    post_id = create_res["post"]["id"]
    print(f"Post criado com sucesso! ID: {post_id}")
    
    # 2. Aprovar o post
    print(f"\n2. Aprovando o post {post_id}...")
    approve_res = social_publisher.approve_post(post_id, approved_by="test_script")
    
    if not approve_res.get("success"):
        print("FALHA AO APROVAR POST:")
        pprint(approve_res)
        return
        
    print("Post aprovado com sucesso!")
    
    # 3. Publicar na NewPost-IA
    print(f"\n3. Publicando o post {post_id} na NewPost-IA...")
    publish_res = social_publisher.publish_to_newpost(post_id)
    
    print("\n=== RESULTADO DA PUBLICAÇÃO ===")
    pprint(publish_res)

if __name__ == "__main__":
    test_flow()
