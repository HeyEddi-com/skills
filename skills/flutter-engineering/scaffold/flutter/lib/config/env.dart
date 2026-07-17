/// API base URL: FastAPI default HeyEddi port 8090.
/// Web: use same host with port 8090 or configure reverse proxy.
const String kApiBaseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'http://127.0.0.1:8090',
);

const int kDefaultApiPort = 8090;
const int kDefaultWebPort = 8085;
