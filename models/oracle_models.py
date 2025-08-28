from oracle_connection import oracle_db
import logging

logger = logging.getLogger(__name__)

class ClienteOracle:
    """Modelo para a view VW_MEGAFEIRAO_LOGCLI"""
    
    @staticmethod
    def get_by_cnpj(cnpj):
        """Busca cliente por CNPJ"""
        cnpj_clean = cnpj.replace('.', '').replace('/', '').replace('-', '')
        logger.info(f"Buscando cliente no Oracle com CNPJ limpo: {cnpj_clean}")
        
        query = """
        SELECT CODCLI, CGEENTAUX, CLIENTE, LIMCRED, LIMDISP, BLOQUEIO, FILIAL
        FROM VW_MEGAFEIRAO_LOGCLI
        WHERE CGEENTAUX = ?
        """
        
        try:
            result = oracle_db.execute_query(query, [cnpj_clean])
            if result:
                logger.info(f"Cliente encontrado no Oracle: {result[0]['CLIENTE']} (CODCLI: {result[0]['CODCLI']} FILIAL: {result[0]['FILIAL']})")
            else:
                logger.info(f"Nenhum cliente encontrado no Oracle para CNPJ: {cnpj_clean}")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Erro ao buscar cliente por CNPJ no Oracle: {e}", exc_info=True)
            return None
    
    @staticmethod
    def get_by_id(codcli):
        """Busca cliente por código"""
        logger.info(f"Buscando cliente no Oracle por CODCLI: {codcli}")
        
        query = """
        SELECT CODCLI, CGCENT, CLIENTE, LIMCRED, LIMDISP, BLOQUEIO, FILIAL
        FROM VW_MEGAFEIRAO_LOGCLI
        WHERE CODCLI = ?
        """
        
        try:
            result = oracle_db.execute_query(query, [codcli])
            if result:
                logger.info(f"Cliente encontrado no Oracle por ID: {result[0]['CLIENTE']} (CNPJ: {result[0]['CGCENT']})")
            else:
                logger.info(f"Nenhum cliente encontrado no Oracle para CODCLI: {codcli}")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Erro ao buscar cliente por ID no Oracle: {e}", exc_info=True)
            return None


class PlanosPagamentoOracle:
    """Modelo para a view VW_MEGAFEIRAO_PLPAG"""
    
    @staticmethod
    def get_by_cliente(codcli):
        """Busca planos de pagamento disponíveis para um cliente"""
        logger.info(f"Buscando planos de pagamento para CODCLI: {codcli}")
        
        query = """
        SELECT CODCLI, FANTASIA, NUMDIASCLI, CODPLPAG, NUMDIAS, 
               DESCRPLPAG, NUMPARCELAS, PRAZO1, PRAZO2, PRAZO3, PRAZO4
        FROM VW_MEGAFEIRAO_PLPAG
        WHERE CODCLI = ?
        ORDER BY NUMDIAS
        """
        
        try:
            result = oracle_db.execute_query(query, [codcli])
            if result:
                logger.info(f"Encontrados {len(result)} planos para CODCLI: {codcli}")
            else:
                logger.info(f"Nenhum plano encontrado para CODCLI: {codcli}")
            return result if result else []
        except Exception as e:
            logger.error(f"Erro ao buscar planos de pagamento no Oracle: {e}", exc_info=True)
            return []
    
    @staticmethod
    def get_plano_by_id(codplpag):
        """Busca um plano específico por código"""
        logger.info(f"Buscando plano de pagamento por CODPLPAG: {codplpag}")
        
        query = """
        SELECT CODCLI, FANTASIA, NUMDIASCLI, CODPLPAG, NUMDIAS, 
               DESCRPLPAG, NUMPARCELAS, PRAZO1, PRAZO2, PRAZO3, PRAZO4
        FROM VW_MEGAFEIRAO_PLPAG
        WHERE CODPLPAG = ?
        """
        
        try:
            result = oracle_db.execute_query(query, [codplpag])
            if result:
                logger.info(f"Plano encontrado: {result[0]['DESCRPLPAG']}")
            else:
                logger.info(f"Nenhum plano encontrado para CODPLPAG: {codplpag}")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Erro ao buscar plano por ID no Oracle: {e}", exc_info=True)
            return None
