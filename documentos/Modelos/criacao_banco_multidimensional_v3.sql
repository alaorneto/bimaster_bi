
CREATE TABLE public.dim_favorecido_transacao (
                sk_favorecido_transacao INTEGER NOT NULL,
                nk_favorecido VARCHAR(20) NOT NULL,
                tipo_atividade VARCHAR(300) NOT NULL,
                nm_favorecido VARCHAR(200) NOT NULL,
                nm_municipio VARCHAR(100),
                uf_favorecido VARCHAR(2),
                CONSTRAINT sk_favorecido_transacao PRIMARY KEY (sk_favorecido_transacao)
);
COMMENT ON COLUMN public.dim_favorecido_transacao.nk_favorecido IS 'CPF ou CNPJ do Favorecido';
COMMENT ON COLUMN public.dim_favorecido_transacao.nm_favorecido IS 'Nome do favorecido pelo Gasto';


CREATE TABLE public.dim_responsavel_transacao (
                sk_responsavel_transacao INTEGER NOT NULL,
                nk_orgao_superior INTEGER NOT NULL,
                nk_orgao INTEGER NOT NULL,
                nk_unidade_gestora INTEGER NOT NULL,
                cpf_portador VARCHAR(20),
                nm_orgao_superior VARCHAR(200) NOT NULL,
                nm_orgao VARCHAR(200) NOT NULL,
                nm_unidade VARCHAR(200) NOT NULL,
                nm_portador VARCHAR(200) NOT NULL,
                CONSTRAINT sk_responsavel_transacao PRIMARY KEY (sk_responsavel_transacao)
);
COMMENT ON TABLE public.dim_responsavel_transacao IS 'Tabela Dimensão com quem é responsável pelo gasto do Cartão de Pagamento do Governo Federal (CPGF).';
COMMENT ON COLUMN public.dim_responsavel_transacao.cpf_portador IS 'CPF parcial do portador';
COMMENT ON COLUMN public.dim_responsavel_transacao.nm_orgao_superior IS 'Nome do órgão superior';
COMMENT ON COLUMN public.dim_responsavel_transacao.nm_orgao IS 'Nome do órgão';
COMMENT ON COLUMN public.dim_responsavel_transacao.nm_unidade IS 'Nome da Unidade Gestora';
COMMENT ON COLUMN public.dim_responsavel_transacao.nm_portador IS 'Nome do Portador do CPGF';


CREATE SEQUENCE public.dim_tempo_sk_tempo_seq;

CREATE TABLE public.dim_tempo (
                sk_tempo INTEGER NOT NULL DEFAULT nextval('public.dim_tempo_sk_tempo_seq'),
                nk_tempo DATE NOT NULL,
                dia INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                ano INTEGER NOT NULL,
                dia_da_semana VARCHAR(30) NOT NULL,
                ano_eleitoral VARCHAR(10) NOT NULL,
                esfera_eleicao VARCHAR(20) NOT NULL,
                CONSTRAINT sk_tempo PRIMARY KEY (sk_tempo)
);
COMMENT ON COLUMN public.dim_tempo.ano_eleitoral IS 'Sim- Quando ocorrem eleições no ano
Não - Ano sem eleições';


ALTER SEQUENCE public.dim_tempo_sk_tempo_seq OWNED BY public.dim_tempo.sk_tempo;

CREATE SEQUENCE public.ft_transacao_sk_ft_transacao_seq;

CREATE TABLE public.ft_transacao (
                sk_ft_transacao INTEGER NOT NULL DEFAULT nextval('public.ft_transacao_sk_ft_transacao_seq'),
                sk_responsavel_transacao INTEGER NOT NULL,
                sk_tempo INTEGER NOT NULL,
                sk_favorecido_transacao INTEGER NOT NULL,
                valor REAL NOT NULL,
                tipo VARCHAR(50) NOT NULL,
                CONSTRAINT sk_transacao PRIMARY KEY (sk_ft_transacao, sk_responsavel_transacao, sk_tempo, sk_favorecido_transacao)
);
COMMENT ON TABLE public.ft_transacao IS 'Tabela com as transações do Cartão de Pagamento do Governo Federal (CPGF).';
COMMENT ON COLUMN public.ft_transacao.tipo IS 'Tipo de transação';


ALTER SEQUENCE public.ft_transacao_sk_ft_transacao_seq OWNED BY public.ft_transacao.sk_ft_transacao;

ALTER TABLE public.ft_transacao ADD CONSTRAINT dim_favorecido_gasto_ft_transacao_fk
FOREIGN KEY (sk_favorecido_transacao)
REFERENCES public.dim_favorecido_transacao (sk_favorecido_transacao)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.ft_transacao ADD CONSTRAINT dim_responsavel_gasto_ft_transacao_fk
FOREIGN KEY (sk_responsavel_transacao)
REFERENCES public.dim_responsavel_transacao (sk_responsavel_transacao)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.ft_transacao ADD CONSTRAINT dim_tempo_ft_transacao_fk
FOREIGN KEY (sk_tempo)
REFERENCES public.dim_tempo (sk_tempo)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
