from config.try_login import try_login
from conexao-bot/src/config import (
    get_connect_buttons, process_connect_button, go_to_next_page
)
from config.linkedin_search import LinkedInSearch
from playwright.sync_api import sync_playwright
from config.web_scraper_profiles import scrape_profiles, save_to_bank, load_connection_count, save_connection_count



MAX_CONNECTIONS = 200

def main():
    # Manage the Playwright instance in a single with block
    with sync_playwright() as p:
        # Attempt to log in and get the page and browser objects
        success, page, browser = try_login(p)

        # Check if login was successful
        if success:
            print("Login attempt: Success")

            # Initialize the LinkedInSearch class and set search keywords
            search = LinkedInSearch("tech Recruiter", "1")
            search_url = search.get_url()
            print(f"Navigating to search URL: {search_url}")

            # Navigate to the search URL using the page object
            page.goto(search_url)
            page.wait_for_load_state("domcontentloaded")

            # Example: Print the page title
            title = page.title()
            print(f"Page title: {title}")

            #Coletar perfis apenas uma vez, no início
            print("Executando WebScraperProfile inicial...")
            scraped_profiles = scrape_profiles(page)
            save_to_bank(scraped_profiles)

            # Carrega o total de conexões já feitas (por exemplo, de um arquivo ou variável persistida)
            connections_made = load_connection_count() or 0

            # Itera no máximo por 100 páginas de resultados
            for page_num in range(1, 101):  # Itera da página 1 até 100
                search.set_page(page_num)
                url = search.get_url()
                page.goto(url)  # Navega para a URL da página atual

                try:
                    # Aguarda um elemento de resultado aparecer para garantir que a página carregou
                    page.wait_for_selector("div[data-chameleon-result-urn]")
                except Exception:
                    print(f"[!] Nenhum conteúdo de perfil carregado na página {page_num}. Encerrando busca.")
                    break

                # Obtém todos os botões "Conectar" presentes na página
                connect_buttons = get_connect_buttons(page)
                if not connect_buttons:
                    # Nenhum convite possível nessa página
                    print(f"[→] Página {page_num}: 0 conexões encontradas.")
                else:
                    conexoes_feitas_na_pagina = 0
                    for button in connect_buttons:
                        process_connect_button(button, page)  # Envia solicitação de conexão
                        conexoes_feitas_na_pagina += 1
                        connections_made += 1
                        if connections_made >= MAX_CONNECTIONS:
                            break  # Atingiu 200 conexões no total, sai do loop interno
                    print(f"[✔] Página {page_num}: {conexoes_feitas_na_pagina} conexões feitas.")

                # Verifica critérios de parada após processar a página
                if connections_made >= MAX_CONNECTIONS:
                    print(f"[✔] Limite de {MAX_CONNECTIONS} conexões atingido. Encerrando o processo.")
                    break

                # Pausa de 0,5s antes de carregar a próxima página
                page.wait_for_timeout(500)

if __name__ == "__main__":
    main()