const LogItem = require('../models/LogItem')


function getClientIp(req) {
    return req.headers['x-forwarded-for'] ||
        req.connection.remoteAddress ||
        req.socket.remoteAddress ||
        req.connection.socket.remoteAddress;
}


const endMiddleware = (req, res, next) => {
    const defaultWrite = res.write;
    const defaultEnd = res.end;
    const chunks = [];
    res.write = (...restArgs) => {
        chunks.push(Buffer.from(restArgs[0]));
        defaultWrite.apply(res, restArgs);
    };
    res.end = async (...restArgs) => {
        let mList = ["POST", "GET"]
        if (mList.indexOf(req.method) !== -1) {
            if (restArgs[0]) {
                chunks.push(Buffer.from(restArgs[0]));
            }
            const body = Buffer.concat(chunks).toString('utf8');
            const time = new Date();

            const Log = new LogItem({
                user_id: (req.user._id) ? req.user._id : null,
                url: req.url,
                method: req.method,
                body: JSON.stringify(req.body),
                params: "",
                ip_address: getClientIp(req),
                result: JSON.stringify(body),
                create_time: time,
                updated_time: time,
            })
            await Log.save();
        }
        defaultEnd.apply(res, restArgs);
    };
    next();
};

module.exports = endMiddleware;
