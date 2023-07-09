import mysql from 'mysql2/promise';
import {ApiPromise, WsProvider} from "@polkadot/api";
import { cryptoWaitReady } from '@polkadot/util-crypto';

async function main() {
    const wsProvider = new WsProvider('wss://khala-api.phala.network/ws');
    const api = await ApiPromise.create({
        provider: wsProvider,
    });

    await cryptoWaitReady();

    const connection = await mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: '*****',
        database: '******'
    });

    const [rows] = await connection.execute('SELECT minerAccountId FROM workers');
    connection.end();

    for (let row of rows) {
        const aa = await api.query.phalaComputation.sessions(row.minerAccountId);
        console.log(`For minerAccountId ${row.minerAccountId}, the result is: ${JSON.stringify(aa)}`);
    }
}

main().catch(console.error);
