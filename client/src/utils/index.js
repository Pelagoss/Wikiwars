import mitt from 'mitt';

const m = mitt();

export function isValidJwt (jwt) {
    if (!jwt || jwt.split('.').length < 3) {
        return false
    }
    const data = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    return now < exp
}

export const emitter = {
    $on: (...args) => m.on(...args),
    $once: (...args) => m.once(...args),
    $off: (...args) => m.off(...args),
    $emit: (...args) => m.emit(...args)
}