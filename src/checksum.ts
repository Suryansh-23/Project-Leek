import crypto from 'crypto';
import fs from 'fs';

export default function verifyFileChecksum(
    filePath: string,
    hashURLIndex: number // Use 0 for File-Vault Zip and 1 for python API
): boolean {
    const hashURLS = [
        '4cb313ea0fc16f9b7fd78e498686ce886579ea21ff9ba4afafc08e2c1c43cf01',
        'a735ee27e06dc1424037f32da21dbc8102d92a77d06ec0ef91c28d6e7e0c0371',
    ];

    const fileBuffer = fs.readFileSync(filePath);

    const sha256sum = crypto.createHash('sha256');
    sha256sum.update(fileBuffer);

    const genHash = sha256sum.digest('hex');

    return hashURLS[hashURLIndex] === genHash;
}
