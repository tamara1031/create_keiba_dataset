CREATE DATABASE IF NOT EXISTS raw_data;
GRANT ALL ON raw_data.* TO 'test'@'%';

USE raw_data;

CREATE TABLE raw_races
(
    id BIGINT NOT NULL AUTO_INCREMENT,
    netkeiba_race_id BIGINT NOT NULL,
    scraped_at BIGINT DEFAULT NULL,
    created_at BIGINT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (netkeiba_race_id),
    INDEX idx_netkeiba_race_id (netkeiba_race_id),
    INDEX idx_scraped_at (scraped_at),
    INDEX idx_created_at (created_at)
);

CREATE TABLE raw_race_informations
(
    id BIGINT NOT NULL AUTO_INCREMENT,
    raw_race_id BIGINT NOT NULL,
    race_number VARCHAR(32) NOT NULL,
    race_condition VARCHAR(32) NOT NULL,
    weather VARCHAR(32) NOT NULL,
    track_condition VARCHAR(32) NOT NULL,
    starting_time VARCHAR(32) NOT NULL,
    race_date VARCHAR(32) NOT NULL,
    event_name VARCHAR(32) NOT NULL,
    race_class VARCHAR(32) NOT NULL,
    race_type VARCHAR(32) NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_raw_race_id (raw_race_id)
);

CREATE TABLE raw_race_results
(
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主キー',
    raw_race_id BIGINT NOT NULL,
    `rank` VARCHAR(32) NOT NULL COMMENT '順位',
    frame_number VARCHAR(32) NOT NULL COMMENT '枠番',
    horse_number VARCHAR(32) NOT NULL COMMENT '馬番',
    horse_name VARCHAR(32) NOT NULL COMMENT '馬名',
    netkeiba_horse_id VARCHAR(32) NOT NULL COMMENT 'ウマID',
    horse_gender_age VARCHAR(32) NOT NULL COMMENT '性齢',
    carried_weight VARCHAR(32) NOT NULL COMMENT '斤量',
    jockey_name VARCHAR(32) NOT NULL COMMENT 'ジョッキー名',
    netkeiba_jockey_id VARCHAR(32) NOT NULL COMMENT 'ジョッキーID',
    `time` VARCHAR(32) NOT NULL COMMENT 'タイム',
    diff VARCHAR(32) NOT NULL COMMENT '着差',
    passing VARCHAR(32) NOT NULL COMMENT '通過',
    final_furlong_time VARCHAR(32) NOT NULL COMMENT '上がり',
    win_odds VARCHAR(32) NOT NULL COMMENT '単勝',
    favorite VARCHAR(32) NOT NULL COMMENT '人気',
    `weight` VARCHAR(32) NOT NULL COMMENT '馬体重',
    trainer VARCHAR(32) NOT NULL COMMENT '調教師',
    netkeiba_trainer_id VARCHAR(32) NOT NULL COMMENT '調教師ID',
    `owner` VARCHAR(32) NOT NULL COMMENT '馬主',
    netkeiba_owner_id VARCHAR(32) NOT NULL COMMENT 'オーナーID',
    prize VARCHAR(32) NULL COMMENT '賞金',
    PRIMARY KEY (id),
    INDEX idx_raw_race_id (raw_race_id)
)
COMMENT='レース結果テーブル';

CREATE TABLE raw_race_payouts
(
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主キー',
    raw_race_id BIGINT NOT NULL,
    payout_type VARCHAR(32) NOT NULL COMMENT '単勝/複勝etc',
    horse_number VARCHAR(32) NOT NULL COMMENT '馬番',
    payout VARCHAR(32) NOT NULL COMMENT 'payout/100yen',
    favorite VARCHAR(32) NOT NULL COMMENT '人気',
    PRIMARY KEY (id),
    INDEX idx_raw_race_id (raw_race_id)
)
COMMENT='レース結果テーブル';