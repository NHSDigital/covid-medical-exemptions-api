import { v4 as uuid } from 'uuid';

export async function logging(req, res, next) {
    res.locals.started_at = Date.now();
    res.locals.correlation_id = (
        req.header('X-Correlation-ID')
        || req.header('Correlation-ID')
        || req.header('CorrelationID')
        || uuid()
    );
    
    const start = new Date();
    try {
        await Promise.resolve(next());
    } catch (err) {
        console.log(err.message);
    } finally {
        const duration = new Date() - start;
        console.log(`${req.method} ${req.originalUrl} ${duration}ms`);
    }
}

export function notFound(req, res) {
    res.status(404).json({ message: 'Not Found' });
}

export function errorHandler(err, req, res, next) {
    res.status(err.statusCode || 500).json({ message: err.message || 'System Error' });
}
